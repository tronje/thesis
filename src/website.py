from score import Score


class Site(object):
    def __init__(self, url):
        assert type(url) is str

        self.url = url
        self.score = Score()
