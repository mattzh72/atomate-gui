from atomate_gui.app import app, collection
from atomate_gui.components.table import CollectionTable
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from io import BytesIO
import base64

from pymongo import MongoClient
from atomate.vasp.database import VaspCalcDb
from sumo.electronic_structure.dos import get_pdos
from sumo.plotting.bs_plotter import SBSPlotter
from sumo.plotting.dos_plotter import SDOSPlotter

class InfoApp:
    default_display_fields = [
        'spacegroup.number',
        'spacegroup.crystal_system',
        'bandstructure.is_metal',
        'structure.lattice.volume',
        'bandstructure.bandgap',
        'bandstructure.is_gap_direct'
    ]

    db_creds = {"host": "localhost", "port": 27017,
             "database": "thermoelectrics", "username": None,
             "password": None}

    @staticmethod
    def serve_layout(pathname):
        result = InfoApp.plot_bs(InfoApp.db_creds, "m-2")
        print(type(result))
        entry = InfoApp.get_entry(pathname)

        return html.Div(children=[
            html.H1(
                children="Structure " + entry['material_id'],
                style={
                    'width': '100%',
                    'margin-bottom': '10px',
                    'text-align': 'center'
                }
            ),
            html.Div(
                InfoApp.generate_dropdown(entry),
                style={
                    'width': '50%',
                    'margin-bottom': '20px',
                    'text-align': 'center',
                    'margin-left': '25%',
                }),
            html.Div(id='info-table'),
        ], id='info-wrapper')

    @staticmethod
    def get_entry(pathname):
        material_id = pathname[1:]
        query = {'material_id': material_id}
        return collection.find(query)[0]

    @staticmethod
    def generate_dropdown(entry):
        flat_entry = CollectionTable.flatten(entry)
        options = []
        for post in flat_entry:
            if post[:1] != "_":
                options.append({
                    'label': post, 'value': post
                })

        return dcc.Dropdown(
            id='info-dropdown',
            options=options,
            multi=True,
            value=InfoApp.default_display_fields,
            placeholder="Select query fields...",
        )

    @staticmethod
    def get_dict_value(entry, flat_name):
        keys = flat_name.split(".")
        value = entry

        for key in keys:
            value = value[key]

        return value

    @staticmethod
    def generate_data_table(pathname, values):
        display_fields = {}
        entry = InfoApp.get_entry(pathname)

        for value in values:
            display_fields[value] = InfoApp.get_dict_value(entry, value)

        return CollectionTable.generate_details_table(display_fields)

    @staticmethod
    def plot_bs(db_credentials, material_id, task_query=None, filename=None,
                        **plot_kwargs):
        task_query = task_query if task_query else {}

        # get database connections
        db = MongoClient(db_credentials["host"],
                         db_credentials["port"])[db_credentials["database"]]
        # db.authenticate(db_credentials["username"], db_credentials["password"])
        calc_db = VaspCalcDb(db_credentials["host"], db_credentials["port"],
                             db_credentials["database"], "tasks",
                             db_credentials["username"], db_credentials["password"])

        material_result = db.materials.find_one({"material_id": material_id})
        if not material_result:
            raise RuntimeError("Material id not found in database: {}".format(
                material_id))

        tasks_ids = [int(tid.split("-")[-1])
                     for tid in material_result["_tasksbuilder"]["all_task_ids"]]
        # get all band structure tasks
        bs_query = {"task_id": {"$in": tasks_ids},
                    "task_label": {"$in": ["nscf line"]}}
        bs_query.update(task_query)
        bs_tasks = list(db.tasks.find(bs_query))
        print(bs_tasks)
        if not bs_tasks:
            raise RuntimeError("No band structure available for: {}".format(
                material_id))

        # get the band structure of the last band structure task
        band_structure = calc_db.get_band_structure(task_id=bs_tasks[-1]["task_id"])
        bs_plotter = SBSPlotter(band_structure)

        # get the DOS tasks
        dos_query = {"task_id": {"$in": tasks_ids},
                     "task_label": {"$in": ["nscf uniform"]}}
        dos_query.update(task_query)
        dos_tasks = list(db.tasks.find(dos_query))

        if dos_tasks:
            # get the DOS for the last DOS task
            dos = calc_db.get_dos(task_id=dos_tasks[-1]["task_id"])
            pdos = get_pdos(dos)

            # generate a combined DOS and band structure plot
            dos_plotter = SDOSPlotter(dos, pdos)

            # set some better defaults for BS+DOS plots but don't overwrite user
            # settings
            if not 'dos_aspect' in plot_kwargs:
                plot_kwargs['dos_aspect'] = 4

            if not 'width' in plot_kwargs:
                plot_kwargs['width'] = 8

            plt = bs_plotter.get_plot(dos_plotter=dos_plotter, **plot_kwargs)

        else:
            # if no DOS just plot band structure only
            plt = bs_plotter.get_plot(**plot_kwargs)

        if filename:
            plt.savefig(filename, dpi=400, bbox_inches='tight')
            return plt

        else:
            figfile = BytesIO()
            plt.savefig(figfile, format='png', dpi=400, bbox_inches='tight')

            # rewind to beginning of file and base64 encode
            figfile.seek(0)
            figdata_png = base64.b64encode(figfile.getvalue())
            return figdata_png


@app.callback(Output('info-table', 'children'),
              [Input('url', 'pathname'),
               Input('info-dropdown', 'value')])
def display_data_table(pathname, values):
    if not pathname or len(pathname) <= 1 or pathname == '/search' or not values:
        raise PreventUpdate
    else:
        return InfoApp.generate_data_table(pathname, values)
