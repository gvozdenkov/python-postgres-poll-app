import configparser

def config(filename = 'database.ini', section = 'postgresql'):
    parser = configparser.RawConfigParser()
    parser.read(filename)
    parser.has_section(section)
    # print(parser.items(section))

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
            # print(f"{param[0]} = {param[1]}")
    else:
        raise Exception('section {0} not found in the {1} file'.format(section, filename))
        
    return db

# config(filename = 'database.ini', section = 'postgresql')