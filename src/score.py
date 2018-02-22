class Score(object):
    def __init__(self):
        self.user_agent = False
        self.language = False
        self.cookie_enabled = False
        self.local_storage = False
        self.session_storage = False
        self.color_depth = False
        self.platform = False
        self.do_not_track = False
        self.cpu = False

        self.font_count = 0
        self.measure_count = 0

        self.max_canvas_width = 0
        self.max_canvas_height = 0

        self.to_data_url = False
        self.get_image_data = False

        self.create_data_channel = False
        self.create_offer = False
        self.onicecandidate = False

        # self.fp_canvas = False
        # self.fp_font = False
        # self.fp_webrtc = False

    def __eq__(self, other):
        if type(self) != type(other):
            return False

        for key in self.__dict__:
            if self.__dict__[key] != other.__dict__[key]:
                return False

        return True

    @property
    def value(self):
        score = 0

        # canvas font fingerprinting
        score += self.font_count * 0.05
        score += self.measure_count * 0.05

        # canvas fingerprinting
        if self.max_canvas_width > 16 and self.max_canvas_height > 16:
            if self.to_data_url or self.get_image_data:
                score += 1

        # webrtc fingerprinting
        if self.create_data_channel \
                and self.create_offer \
                and self.onicecandidate:
            score += 1

        if self.user_agent:
            score += 1

        if self.language:
            score += 1

        if self.cookie_enabled:
            score += 1

        if self.local_storage:
            score += 1

        if self.session_storage:
            score += 1

        if self.color_depth:
            score += 1

        if self.platform:
            score += 1

        if self.do_not_track:
            score += 1

        if self.cpu:
            score += 1

        return score
