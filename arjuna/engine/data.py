
def record(**kwargs):
    def call():
        keys = []
        values = []
        for k,v in kwargs.items():
            keys.append(k)
            values.append(v)
        print(",".join(keys), values)
        if len(keys) > 1:
            return ",".join(keys), [values]
        else:
            return ",".join(keys), values
    return call