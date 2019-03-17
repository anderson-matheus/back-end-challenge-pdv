import simplejson

class Config:
    def __init__(self):
        with open('config.json') as json_data_file:
            self.config = simplejson.load(json_data_file)

    def get_config(self):
        return self.config
