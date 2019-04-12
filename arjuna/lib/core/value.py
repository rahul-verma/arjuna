import re
import abc

class UnsupportedRepresentationException(Exception):

    def __init__(self, strSourceValue, targetValueType):
        super("Value: Can not represent value >>{}<< as {}.".format(strSourceValue, targetValueType))


class AnyRefValue:
    TRUES = {"YES", "TRUE", "ON", "1"}
    FALSES = {"NO", "FALSE", "OFF", "0"}

    def __init__(self, obj):
        # if type(obj) is str:
        #     obj = obj.encode("utf-8")
        # print(obj, type(obj))
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


class EmptyValueMapLookUpException:

    def __init__(self, key):
        super().__init__("Invalid key [{}] used for ValueMap lookup. It is empty.".format(key))


class ValueListLookUpException:

    def __init__(self, index, max_index):
        super().__init__("Invalid index [{}] used for ValueList lookup. Use indices between 0 and {}".format(index, max_index))


class ValueMapLookUpException:

    def __init__(self, key):
        super().__init__("Invalid key/header [{}] used for ValueMap lookup.".format(key))


class AbstractValueList:

    def __init__(self, *objects):
        self.__values = []
        self.add_all_objects(*objects)

    def _max_index(self):
        return len(self.__values) - 1

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
            self.add_object(o)

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
        return self.value_at(index).as_string()

    def object_at(self, index):
        return self.value_at(index).object()


class AbstractValueMap(metaclass=abc.ABCMeta):

    def __init__(self, object_map=None, headers=None, objects=None):
        msg = "For creating a value map, either pass raw dict as object_map arg or pass headers & objects args of same length together."
        raw_map = None
        if object_map:
            if headers or objects:
                raise Exception(msg)
            raw_map = object_map
        else:
            if not headers and not objects:
                raw_map = dict()
            else:
                if not headers or not objects:
                    raise Exception(msg)
                elif len(headers) != len(objects):
                    raise Exception(msg)
                else:
                    raw_map = dict(zip(headers, objects))
        self.__map = dict()
        for t,v in raw_map.items():
            self.add_object(t,v)

    def _format_key(self, key):
        return key

    def as_map(self):
        return self.__map

    def keys(self):
        return self.__map.keys()

    @abc.abstractmethod
    def _format_key_as_str(self, key):
        pass

    def items(self, filter_keys=None):
        if not filter_keys:
            return self.__map

        self.__validate_keys(filter_keys)
        fkeyset = set(filter_keys)
        return {k: v for k, v in self.__map.items() if k in fkeyset}

    def __validate_key(self, key):
        if not self.__map:
            raise EmptyValueMapLookUpException(self._format_key_as_str(key))
        elif key not in self.__map:
            raise ValueMapLookUpException(self._format_key_as_str(key))

    def __validate_keys(self, keys):
        for key in keys:
            self.__validate_key(key)

    def __convert_to_string_map(self, map):
        return {self._format_key_as_str(k): v.as_string() for k,v in self.__map.items()}

    def str_items(self, filter_keys=None):
        if not filter_keys:
            return self.__convert_to_string_map(self.__map)
        else:
            return self.__convert_to_string_map(self.items(filter_keys))

    def value(self, key):
        self.__validate_key(key)
        return self.__map[key]

    def object(self, key):
        self.__validate_key(key)
        return self.__map[key].object()

    def string(self, key):
        self.__validate_key(key)
        return self.__map[key].as_string()

    def has_key(self, key):
        return self._format_key(key) in self.__map

    def add(self, key, value):
        self.__map[self._format_key(key)] = value

    def add_object(self, key, obj):
        self.__map[self._format_key(key)] = AnyRefValue(obj)

    def add_all(self, map):
        for k,v in map.items():
            self.add(k,v)

    def add_all_objects(self, map):
        for k, v in map.items():
            self.add_object(k, map.get(v))


class StringKeyValueMap(AbstractValueMap):

    def __init__(self, object_map=None, headers=None, objects=None):
        super().__init__(object_map, headers, objects)

    def _format_key(self, key):
        return key.lower().strip()

    def _format_key_as_str(self, key):
        return key




