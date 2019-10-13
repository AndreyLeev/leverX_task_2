from functools import total_ordering 

@total_ordering
class Version:
    def __init__(self, version):
        self.version = version
        self.convert()

    def convert(self):
        literal = (('a', '-alpha'),('b','-beta'),('rc','-rc'))
        if self.version.find('-') == -1: 
            for i in literal:
                self.version = self.version.replace(*i)
        if self.version.find('-') != -1:
            self.version_core, self.pre_release = self.version.split('-')
        else:
            self.version_core, self.pre_release = self.version, None

    def __eq__(self, other):
        return self.version == other.version

    def __lt__(self, other):
        if self.version_core != other.version_core:
            return self.version_core < other.version_core
        else: 
            if self.pre_release is None:
                return False
            elif other.pre_release is None:
                return True
            else: 
                return self.pre_release < other.pre_release


def main():
    to_test = [
        ('1.0.0', '2.0.0'),
        ('1.0.0', '1.42.0'),
        ('1.2.0', '1.2.42'),
        ('1.1.0-alpha', '1.2.0-alpha.1'),
        ('1.0.1b', '1.0.10-alpha.beta'),    
        ('1.0.0-rc.1', '1.0.0'),
        ('1.2.0-alpha.5', '1.2.0-alpha.beta'),
        ('1.0.0-alpha.beta', '1.0.0'),
    ]

    for version_1, version_2 in to_test:
       assert Version(version_1) < Version(version_2), 'le failed'
       assert Version(version_2) > Version(version_1), 'ge failed'
       assert Version(version_2) != Version(version_1), 'neq failed'
    

if __name__ == "__main__":
    main()
