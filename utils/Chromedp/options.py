class Options(object):
    def __init__(self):
        self.arguments = ['chrome']

    def add_argument(self, option):
        self.arguments.append(option)
