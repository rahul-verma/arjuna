
class DriverElementCommands:

    @classmethod
    def send_text(cls, element, text):
        element.send_keys(text)

    @classmethod
    def clear_text(cls, element):
        element.clear()

    @classmethod
    def submit(cls, element):
        element.submit()

    @classmethod
    def click(cls, element):
        element.click()

    @classmethod
    def get_text_content(cls, element):
        return element.text

    @classmethod
    def get_attr_value(cls, element, attr):
        return element.get_attribute(attr)

    @classmethod
    def get_tag_name(cls, element):
        return element.tag_name

    @classmethod
    def is_displayed(cls, element):
        return element.is_displayed()

    @classmethod
    def is_clickable(cls, element):
        return element.is_enabled()

    @classmethod
    def is_selected(cls, element):
        return element.is_selected()