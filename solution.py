from functools import total_ordering 

@total_ordering
class Version:

    def __init__(self, version):
        self.version = self._convert_to_single_format(version)
        self.version_core, self.rest = self._split_version(self.version) 

    def _convert_to_single_format(self, version):
        literal = (('a', '-alpha'),('b','-beta'),('rc','-rc'))
        if version.find('-') == -1: 
            for i in literal:
                version = version.replace(*i)
        return version

    def _split_version(self, version):

        splited_version = version.replace('-','.').split('.')

        for index, item in enumerate(splited_version):
            if item.isdigit():
                splited_version[index] = int(item)
        
        version_core = splited_version[:3]
        rest = splited_version[3:] if splited_version[3:] else []
        return version_core,rest

    def __eq__(self, other):
        return self.version == other.version

    def __lt__(self, other):
        if self.version_core != other.version_core:
            return self.version_core < other.version_core
        elif self.rest == []:
            return False
        elif other.rest == []:
            return True
        else:
            rest1,rest2 = self.rest,other.rest
            min_len = min(len(rest1), len(rest2))
            for i in range(min_len):
                if type(rest1[i]) == type(rest2[i]):   
                    if rest1[i] != rest2[i]:
                        return rest1[i] < rest2[i]
                elif type(rest1[i]) == int:
                    return True
                else:
                    return False
            return len(rest1) < len(rest2)

def main():
    to_test = [
        ('1.0.0', '12.0.0'),
        ('1.0.0', '1.42.0'),
        ('1.2.0', '1.2.42'),
        ('1.1.0-alpha', '1.2.0-alpha.1'),
        ('1.0.1b', '1.0.10-alpha.beta'),    
        ('1.0.0-rc.1', '1.0.0'),
        ('1.2.0-alpha.5', '1.2.0-alpha.beta'),
        ('1.2.0-alpha.beta', '1.2.0-alpha.beta.5'),
        ('1.2.0-alpha.3', '1.2.0-alpha.5'),
        ('1.2.0a', '1.2.0-alpha.5'),
        ('1.0.0-alpha.beta', '1.0.0rc'),    
        ('1.0.0-alpha.beta', '1.0.0'),
    ]

    for version_1, version_2 in to_test:
        v1 = Version(version_1)
        v2 = Version(version_2)
        assert v1 < v2, 'le failed'
        assert v2 > v1, 'ge failed'
        assert v1 != v2, 'neq failed'
    

if __name__ == "__main__":
    main()
