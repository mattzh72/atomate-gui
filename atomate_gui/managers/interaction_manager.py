class InteractionManager:
    def __init__(self):
        self.search_time = -1
        self.rpp = 50
        self.back_time = -1
        self.fwd_time = -1
        self.max_time = -1

    def check_rpp(self, new_rpp):
        if isinstance(new_rpp, str):
            new_rpp = int(new_rpp)

        if self.rpp == new_rpp:
            return False
        else:
            self.rpp = new_rpp
            return True

    def check_btn(self, s_time, b_time, f_time):
        if not s_time:
            s_time = -1
        if not b_time:
            b_time = -1
        if not f_time:
            f_time = -1

        self.search_time = s_time
        self.back_time = b_time
        self.fwd_time = f_time

        if max(s_time, b_time, f_time) <= self.max_time:
            return False

        return True

    def get_recent_btn(self):
        self.max_time = max(self.search_time, self.back_time, self.fwd_time)
        return self.max_time

