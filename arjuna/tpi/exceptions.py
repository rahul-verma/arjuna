class WaitableError(BaseException):

    def __init__(self, message):
        super().__init__(message)

class GuiElementNotFoundError(WaitableError):

    def __init__(self, message, locator):
        super().__init__("GuiElement(s) not found using locator: {}. Tool message: {}".format(locator, message))

class GuiElementNotReadyError(WaitableError):

    def __init__(self, message):
        super().__init__("GuiElement(s) is/are NOT ready for interaction. Tool message: {}".format(message))

class GuiElementTextNotSetError(WaitableError):

    def __init__(self, message):
        super().__init__(". Tool message: {}".format(message))
