# Fakers

class FakeDataHandler(object):
    def __init__(self, parser, provider):
        pass

    def get_value_for(self, key):
        return True


class FakeParser:
    def parse(self, string):
        return (True, string)


class FakeProvider(object):
    def __init__(self, parser=FakeParser()):
        self.parse = parser.parse

    def get_value_for(self, string):
        return self.parse(string)

