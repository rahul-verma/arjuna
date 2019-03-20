from selenium.webdriver.common.by import By

from .melement import MultiElement

class ElementFinder:
    BY_MAP = {
        "ID": By.ID,
        "NAME": By.NAME,
        "TAG_NAME": By.TAG_NAME,
        "CLASS_NAME": By.CLASS_NAME,
        "LINK_TEXT": By.LINK_TEXT,
        "PARTIAL_LINK_TEXT": By.PARTIAL_LINK_TEXT,
        "CSS_SELECTOR": By.CSS_SELECTOR,
        "XPATH": By.XPATH
    }
    
    @classmethod
    def find_element(cls, container, byType, byValue):
        return container.find_element(cls.BY_MAP[byType.upper()], byValue)

    @classmethod
    def find_elements(cls, container, byType, byValue):
        return MultiElement(container.find_elements(cls.BY_MAP[byType.upper()], byValue))
