# import __builtin__

class EnumDict(dict):
    def where(self, key,filter):
        return filter.lower() in self[key].lower()


class EnumList(list):
    def where(self,key,filter):
        # check if method called where exists in the first element
        if 'where' in dir(self[0]):
            return [x for x in self if x.where(key, filter)]
        raise Exception("Method 'where' not yet implmented for object %s" % (type(self[0])))

__builtins__.dict = EnumDict
__builtins__.list = EnumList
