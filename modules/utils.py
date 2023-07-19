def initValue(data, param, defVal, defVal2=None):
    if param in data:
        data[param] = data[param]
    elif type(defVal) == dict:
        if param in defVal:
            data[param] = defVal[param]
        else:
            data[param] = defVal2
    else:
        data[param] = defVal

def getValue(data, param, defVal, defVal2=None):
    if param in data:
        return data[param]
    elif type(defVal) == dict:
        if param in defVal:
            return defVal[param]
        else:
            return defVal2
    else:
        return defVal
        