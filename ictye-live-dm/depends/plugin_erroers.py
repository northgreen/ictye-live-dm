class PluginTypeError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class UnexpectedPluginMessage(Exception):
    def __init__(self, message):
        super(UnexpectedPluginMessage, self).__init__(message)


class UnexpectedPluginMather(Exception):
    def __init__(self, message):
        super(UnexpectedPluginMather, self).__init__(message)


class NoMainMather(Exception):
    def __init__(self, message):
        super(NoMainMather, self).__init__(message)
