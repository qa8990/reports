from pyjavaproperties import Properties

def read_properties_file(file_path):
    p = Properties()
    p.load(open(file_path))
    #p.list()
    #print(p)
    return p
