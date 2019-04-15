from app import collection
from components.table import CollectionTable
from managers.interaction_manager import InteractionManager
from math import ceil
import ast

class QueryManager:
    default_query = [
        "['nelements']",
        "['material_id']",
        "['spacegroup']['number']",
        "['stability']['e_above_hull']",
        "['bandstructure']['is_gap_direct']",
        "['chemsys']"
    ]
    default_fields = [
        "['chemsys']",
        "['bandgap']",
        "['material_id']"
    ]

    def __init__(self):
        self.pages = []
        self.index = 0
        self.curr_page = None
        self.page_msg = ""
        self.i_manager = InteractionManager()

    def create_message(self):
        if len(self.pages) == 0:
            return "1 of 1"
        else:
            return "{} of {}".format(self.index + 1, len(self.pages))

    def create_table(self, query, fields, rpp, f_time, b_time, s_time):
        if self.i_manager.check_rpp(rpp):
            self.query(query, fields, rpp)
            return CollectionTable.generate_search_table(self.get_first_page())

        if self.i_manager.check_btn(s_time, b_time, f_time):
            recent_btn_time = self.i_manager.get_recent_btn()

            if recent_btn_time == f_time:
                return CollectionTable.generate_search_table(self.get_next_page())
            elif recent_btn_time == b_time:
                return CollectionTable.generate_search_table(self.get_prev_page())
            elif recent_btn_time == s_time:
                self.query(query, fields, rpp)
                return CollectionTable.generate_search_table(self.get_first_page())

        return ""

    def query(self, query, fields, rpp):
        if isinstance(rpp, str):
            rpp = int(rpp)

        # cache the results
        results = [p for p in collection.find(ast.literal_eval(query), ast.literal_eval(fields))]
        self.index = 0
        num_pages = ceil(len(results)/rpp)

        # slice up the results into the proper pages
        self.pages = [results[i * rpp: (i + 1) * rpp] for i in range(num_pages)]

    def get_curr_page(self):
        return self.pages[self.index]

    def get_first_page(self):
        self.index = 0

        if len(self.pages) == 0:
            return ""

        return self.pages[0]

    def get_next_page(self):
        self.index = min(self.index + 1, len(self.pages) - 1)

        return self.pages[self.index]

    def get_prev_page(self):
        self.index = max(self.index - 1, 0)

        return self.pages[self.index]






