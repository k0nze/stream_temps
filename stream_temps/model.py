import json

class JsonFileCreateException(Exception):
    """ raised when json model could not be created """
    pass


class JsonFileOpenException(Exception):
    """ raised when json model could not be opened """
    pass


class JsonFileWriteException(Exception):
    """ raised when json model could not be written """
    pass


class Model():
    def __init__(self, json_path):
        # check if json model exists
        self.json_path = json_path
        self.data = dict()
        
        if not self.json_path.is_file():
            # try to create the json model
            try:
                with open(self.json_path.resolve(), 'w') as json_file:

                    self.data = {
                        'settings': {
                            'temperature_unit': 'C'
                        },
                        'profiles': [
                            {
                                'name': 'default',
                                'index_html': 'index.html',
                                'style.css': 'style.css'
                            }
                        ]
                    }
                            
                
                    json.dump(self.data, json_file, sort_keys=True, indent=4)

            except Exception as e:
                raise JsonFileCreateException 

        # read config
        else: 
            with open(self.json_path.resolve(), 'r') as json_file:
                self.data = json.load(json_file)


