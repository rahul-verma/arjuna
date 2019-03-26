import re


class UnsupportedRepresentationException(Exception):

    def __init__(self, strSourceValue, targetValueType):
        super("Value: Can not represent value >>{}<< as {}.".format(strSourceValue, targetValueType))


class AnyRefValue:
    TRUES = {"YES", "TRUE", "ON", "1"}
    FALSES = {"NO", "FALSE", "OFF", "0"}

    def __init__(self, obj):
        self.__obj = obj
        self.__str_obj = None
        if self.is_none():
            self.__str_obj = "null"
        else:
            self.__str_obj = str(obj).strip()

    def __throw_wrong_repr_exception(self, valueType):
        raise UnsupportedRepresentationException(self.to_string(), valueType)

    def object(self):
        return self.__obj

    def to_string(self):
        return self.__str_obj

    def __fmt_str(self):
        return self.__str_obj.upper().strip()

    as_string = to_string
    __str__ = to_string

    @staticmethod
    def is_set(strValue):
        return not strValue.upper().strip().equals("NOT_SET")

    def is_not_set(self):
        return self.__fmt_str().equals("NOT_SET")

    def is_none(self):
        return self.__obj == None

    is_null = is_none

    def is_na(self):
        return self.__fmt_str().equals("NA")

    def as_enum(self, enumKlass):
        try:
            return enumKlass[self.__fmt_str()]
        except:
            self.__throw_wrong_repr_exception("enum constant of type " + enumKlass.__name__)

    def as_boolean(self):
        fstr = self.__fmt_str()
        if fstr in self.TRUES:
            return True
        elif fstr in self.FALSES:
            return False
        self.__throw_wrong_repr_exception("boolean")

    def as_number(self):
        fstr = self.__fmt_str()
        if re.match(r"(\-)?[0-9\.]+", fstr):
            return float(fstr)
        elif re.match("(\-)?[0-9]+", fstr):
            return int(fstr)
        else:
            self.__throw_wrong_repr_exception("number")

    def as_int(self):
        try:
            return int(self.__fmt_str())
        except:
            self.__throw_wrong_repr_exception("int")

    def as_long(self):
        try:
            return self.asInt()
        except:
            self.__throw_wrong_repr_exception("long")

    def as_float(self):
        try:
            return float(self.__fmt_str())
        except:
            self.__throw_wrong_repr_exception("float")

    def as_double(self):
        try:
            return self.as_float()
        except:
            self.__throw_wrong_repr_exception("double")

    def as_enum_list(self, enumKlass):
        try:
            if type(self.object()) is list:
                return [enumKlass[i] for i in self.object()]
            else:
                return [self.as_enum(enumKlass)]
        except:
            self.__throw_wrong_repr_exception("enum constant list of type " + enumKlass.__name__)

    def as_number_list(self):
        try:
            return [self.as_number()]
        except:
            self.__throw_wrong_repr_exception("number list")

    def as_int_list(self):
        try:
            return [self.as_int()]
        except:
            self.__throw_wrong_repr_exception("int list")

    def as_string_list(self):
        try:
            return [self.as_string()]
        except:
            self.__throw_wrong_repr_exception("string list")

class EmptyValueListLookUpException:

    def __init__(self, index):
        super().__init__("Invalid index [{}] used for ValueList lookup. It is empty.".format(index))

class ValueListLookUpException:

    def __init__(self, index, max_index):
        super().__init__("Invalid index [{}] used for ValueList lookup. Use indices between 0 and {}".format(index, max_index))

class AbstractValueList:

    def __init__(self, *objects):
        self.__values = []
        self.addAllObjects(*objects)

    def _max_index(self):
        return len(self.__values) - 1;

    def __validate_index(self, index):
        if len(self.__values) == 0:
            raise EmptyValueListLookUpException(index)
        else:
            if index > self._max_index():
                raise ValueListLookUpException(index, self._max_index())

    def __validate_indices(self, indices):
        for index in indices:
            self.__validate_index(index)

    def values(self, filter_indices=None):
        if not filter_indices:
            return self.__values
        else:
            self.__validate_indices(filter_indices)
            indices_set = set(filter_indices)
            return [j for i, j in enumerate(self.__values) if i in indices_set]

    def __convert_to_string_list(self, value_list):
        return [v.asString() for v in value_list]

    def strings(self, filter_indices=None):
        considered = None
        if not filter_indices:
            considered = self.__values
        else:
            self.__validate_indices(filter_indices)
            indices_set = set(filter_indices)
            considered = [j for i, j in enumerate(self.__values) if i in indices_set]
        return self.__convert_to_string_list(considered)

    def add_all(self, values):
        self.__values.extend(values)

    def add_all_objects(self, objects):
        for o in objects:
            self.addObject(o)

    def add(self, value):
        self.__values.append(value)

    def add_object(self, obj):
        self.__values.append(AnyRefValue(obj))

    def has_index(self, index):
        return index < self._max_index()

    def value_at(self, index):
        self.__validate_index(index)
        return self.__values[index]

    def string_at(self, index):
        return self.valueAt(index).asString()

    def object_at(self, index):
        return self.objectAt(index).asString()
