class PluginTypeError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class UnexpactedPluginMessage(Exception):
    def __init__(self, message):
        super(UnexpactedPluginMessage, self).__init__(message)
