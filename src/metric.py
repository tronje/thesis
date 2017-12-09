class Metric(object):
    def __init__(
            self,
            canvas_criteria,
            canvas_font_criteria,
            webrtc_criteria,
            audio_criteria,
            battery_criteria
            ):
        self._canvas = canvas_criteria
        self._canvas_font = canvas_font_criteria
        self._webrtc = webrtc_criteria
        self._audio = audio_criteria
        self._battery = battery_criteria

    def __getitem__(self, key):
        return {"canvas": self._canvas,
                "canvas_font": self._canvas_font,
                "webrtc": self._webrtc,
                "audio": self._audio,
                "battery": self._battery,
                }[key]


class DefaultMetric(Metric):
    """Default metric based on Englehardt, et. al.'s findings"""

    def __init__(self):
        self._canvas = {
                "dimensions": [16, 16],
                "colors": 2,
                "chars": 10,
                "excluded_methods": ["save", "restore", "addEventListener"],
                "called_methods": ["toDataURL", "getImageData"],
                "area_size": [16, 16],
                }

        self._canvas_font = {
                "num_fonts": 50,
                "measureText_calls": 50,
                }

        self._webrtc = {
                "called_methods": ["createDataChannel", "createOffer"],
                "event_handler_access": ["onicecandidate"],
                }

        self._audio = None

        self._battery = None
