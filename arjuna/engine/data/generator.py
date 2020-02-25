import uuid
from mimesis import Person
from mimesis import Address
from mimesis import locales
from mimesis import Text
from collections import namedtuple

Locales = locales
Entity = namedtuple

class Random:

    @classmethod
    def ustr(cls, prefix=None):
        prefix = prefix and prefix + "-" or ""
        return "{}{}".format(prefix, uuid.uuid4())

    @classmethod
    def first_name(cls, locale=Locales.EN):
        return Person(locale).first_name()

    @classmethod
    def last_name(cls, locale=Locales.EN):
        return Person(locale).last_name()

    @classmethod
    def phone(cls, locale=Locales.EN):
        return Person(locale).telephone()

    @classmethod
    def email(cls, locale=Locales.EN):
        return Person(locale).email()

    @classmethod
    def street_name(cls, locale=Locales.EN):
        return Address(locale).street_name()

    @classmethod
    def street_number(cls, locale=Locales.EN):
        return Address(locale).street_number()

    house_number = street_number

    @classmethod
    def postal_code(cls, locale=Locales.EN):
        return Address(locale).postal_code()

    @classmethod
    def city(cls, locale=Locales.EN):
        return Address(locale).city()

    @classmethod
    def country(cls, locale=Locales.EN):
        return Address(locale).country()

    @classmethod
    def sentence(cls, locale=Locales.EN):
        return Text(locale).sentence()
        
