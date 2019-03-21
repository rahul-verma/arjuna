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
        if self.isNull():
            self.__str_obj = "null"
        else:
            self.__str_obj = str(obj).strip()

    def __throw_wrong_repr_exception(self, valueType):
        raise UnsupportedRepresentationException(self.toString(), valueType)

    def object(self):
        return self.__obj

    def toString(self):
        return self.__str_obj

    def __fmt_str(self):
        return self.__str_obj.upper().strip()

    asString = toString

    @staticmethod
    def isSet(strValue):
        return not strValue.upper().strip().equals("NOT_SET")

    def isNotSet(self):
        return self.__fmt_str().equals("NOT_SET")

    def isNull(self):
        return self.__obj == None

    def isNA(self):
        return self.__fmt_str().equals("NA")

    def asEnum(self, enumKlass):
        try:
            return enumKlass[self.__fmt_str()]
        except:
            self.__throw_wrong_repr_exception("enum constant of type " + enumKlass.__name__)

    def asBoolean(self):
        fstr = self.__fmt_str()
        if fstr in self.TRUES:
            return True
        elif fstr in self.FALSES:
            return False
        self.__throw_wrong_repr_exception("boolean")

    def asNumber(self):
        fstr = self.__fmt_str()
        if re.match(r"(\-)?[0-9\.]+", fstr):
            return float(fstr)
        elif re.match("(\-)?[0-9]+", fstr):
            return int(fstr)
        else:
            self.__throw_wrong_repr_exception("number")

    def asInt(self):
        try:
            return int(self.__fmt_str())
        except:
            self.__throw_wrong_repr_exception("int")

    def asLong(self):
        try:
            return self.asInt()
        except:
            self.__throw_wrong_repr_exception("long")

    def asFloat(self):
        try:
            return float(self.__fmt_str())
        except:
            self.__throw_wrong_repr_exception("float")

    def asDouble(self):
        try:
            return self.asFloat()
        except:
            self.__throw_wrong_repr_exception("double")

    def asEnumList(self, enumKlass):
        try:
            return [self.asEnum(enumKlass)]
        except:
            self.__throw_wrong_repr_exception("enum constant list of type " + enumKlass.__name__)

    def asNumberList(self):
        try:
            return [self.asNumber()]
        except:
            self.__throw_wrong_repr_exception("number list")

    def asIntList(self):
        try:
            return [self.asInt()]
        except:
            self.__throw_wrong_repr_exception("int list")

    def asStringList(self):
        try:
            return [self.asString()]
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

    def addAll(self, values):
        self.__values.extend(values)

    def addAllObjects(self, objects):
        for o in objects:
            self.addObject(o)

    def add(self, value):
        self.__values.append(value)

    def addObject(self, obj):
        self.__values.append(AnyRefValue(obj))

    def hasIndex(self, index):
        return index < self._max_index()

    def valueAt(self, index):
        self.__validate_index(index)
        return self.__values[index]

    def stringAt(self, index):
        return self.valueAt(index).asString()

    def objectAt(self, index):
        return self.objectAt(index).asString()
