import readline

class Completer:
    def __init__(self):
        self.permalinks = []
        self.words = {
            "play": self.permalinks,
            "get": {
                "coub": self.permalinks,
                "hot": None,
                "newest": None
            },
            "next": None,
            "quit": None
        }
        self.line = None


    def complete(self, prefix, index):
        line = readline.get_line_buffer()
        
        if line != self.line:
            self.matching_words = self.__get_nested(self.words, line)
            self.line = line
            
        try:
            return self.matching_words[index]
        except IndexError:
            return None

    def push_coub(self, permalink):
        self.permalinks.append(permalink)


    def __get_nested(self, obj, attr, default = []):
        attributes = attr.split(' ')
        att_len = len(attributes) - 1
        
        for i, k in enumerate(attributes):
            try:
                if i < att_len:
                    obj = obj[k]
                else:
                    return [w for w in obj if w.startswith(k)]
            except AttributeError:
                return default
        
        return obj.keys() if obj else default
