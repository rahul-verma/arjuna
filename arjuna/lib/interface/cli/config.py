

class CliArgsConfig:

    def __init__(self, arg_dict):
        print(arg_dict)
        self.__aco = {}
        self.__ato = {}
        self.__uco = {}
        self.__uto = {}

        kinds = {
            "aco": self.__aco,
            "ato": self.__ato,
            "uco": self.__uco,
            "uto": self.__uto
        }

        lower_actual_key_map = {i.lower():i for i in arg_dict}
        for kind in kinds:
            if kind in lower_actual_key_map:
                actual_key = lower_actual_key_map[kind]
                d_item = arg_dict[actual_key]
                if d_item:
                    for entry in d_item:
                        k,v = entry
                        kinds[kind][k.lower()] = v
                del arg_dict[actual_key]

        for akey, avalue in arg_dict.items():
            self.__aco[akey.lower()] = avalue

        print(self.__aco)
        print(self.__ato)
        print(self.__uco)
        print(self.__uto)

    def as_map(self):
        return {
            "arjunaCentralOptions": self.__aco,
            "arjunaTestOptions": self.__ato,
            "userCentralOptions": self.__uco,
            "userTestOptions": self.__uto
        }

