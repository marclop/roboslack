class SlackAPIKeyNotSpecified(Exception):
    """Raise excepcion when the Slack API Key is not specified"""

    def __init__(self):
        super(SlackAPIKeyNotSpecified, self).__init__(self)
        self.message = "Slack API Key not specified"


class ClientCannotBeEmptyException(Exception):
    """Raise excepcion when the Slack API Key is not specified"""

    def __init__(self):
        super(ClientCannotBeEmptyException, self).__init__(self)
        self.message = "Slack client cannot be empty"


class InvalidMessageType(Exception):
    """Raise excepcion when the Slack API Key is not specified"""

    def __init__(self, arg):
        super(InvalidMessageType, self).__init__(self)
        self.message = "Invalid essage type {}".format(arg)
