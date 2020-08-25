import json
import socket

from .consts import *

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
                            'temperature_system': 'C'
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

        self.observers = []

    def register_observer(self, observer):
        self.observers.append(observer)

    def __notify_observers(self):
        for observer in self.observers:
            observer.notify()

    def __save_json(self):
        try:
            with open(self.json_path.resolve(), 'w') as json_file:
                json.dump(self.data, json_file, sort_keys=True, indent=4)

        except Exception as e:
            raise JsonFileWriteException

    def __name_filter(self, string):
        # filter out restricted characters 
        # 0-9 (48-57)
        # A-Z (65-90)
        # a-z (97-122)
        return ''.join([i if (ord(i) >= 48 and ord(i) <= 57) or (ord(i) >= 65 and ord(i) <= 90) or (ord(i) >= 97 and ord(i) <= 122) else '' for i in string]).lower()

    def get_temperature_system(self):
        return self.data['settings']['temperature_system']

    def set_temperature_system(self, temperature_system):
        if temperature_system == "C" or temperature_system == "F":
            self.data['settings']['temperature_system'] = temperature_system
            self.__save_json()
            self.__notify_observers()


    def get_profile_names(self):
        profile_names = []     
        for profile in self.data['profiles']:
            profile_names.append(profile['name'])

        return sorted(profile_names, key=str.casefold)

    def get_default_profile_name(self):
        profile_names = self.get_profile_names()

        if "Default" in profile_names:
            return "Default"

        return profile_names[0]

    def add_profile(self, profile_name):
        # check if name already exists 
        profile_names = self.get_profile_names()

        if profile_name in profile_names:
            number = 2
            while profile_name + " " + str(number) in profile_names:
                number = number + 1 

            profile_name = profile_name + " " + str(number)

        # TODO name for index and style
        # TODO create index and style
        self.data['profiles'].append({
            'name': profile_name,
            'index_html': 'index_' + self.__name_filter(profile_name) + '.html',
            'style_css': 'style_' + self.__name_filter(profile_name) + '.css'
        })

        self.__save_json()
        self.__notify_observers()

    def delete_profile(self, profile_name):
        if profile_name != self.get_default_profile_name():
            new_profiles = []
           
            for profile in self.data['profiles']:
                if profile['name'] != profile_name:
                    new_profiles.append(profile)

            self.data['profiles'] = new_profiles

            self.__save_json()
            self.__notify_observers()

    def get_profile_index_html_file(self, profile_name):
        for profile in self.data['profiles']:
            if profile_name == profile['name']:
                return profile['index_html']

        return 'index.html'


    def get_html(self):
        # read root_dir/index.html
        index_html_file = open(ROOT_DIR + "/index.html", "r")
        index_html = index_html_file.read()
        index_html_file.close()
        
        # remove wrapper
        wrapper_index_html_file = open(TEMPLATES_DIR + "/wrapper_index.html", "r")
        wrapper_index_html = wrapper_index_html_file.read().split("$(CONTENT)")
        wrapper_index_html_file.close()

        wrapper_index_html_top = wrapper_index_html[0]
        wrapper_index_html_bottom = wrapper_index_html[1]

        index_html = index_html.replace(wrapper_index_html_top, '') 
        index_html = index_html.replace(wrapper_index_html_bottom, '') 

        return index_html

    def get_css(self):
        # read root_dir/style.css
        style_css_file = open(ROOT_DIR + "/style.css", "r")
        style_css = style_css_file.read()
        style_css_file.close()

        # remove wrapper
        wrapper_style_css_file = open(TEMPLATES_DIR + "/wrapper_style.css", "r")
        wrapper_style_css = wrapper_style_css_file.read().replace("\n$(CONTENT)", "")
        wrapper_style_css_file.close()

        style_css = style_css.replace(wrapper_style_css, "")

        return style_css

    def save_profile(self, html, css):
        # apply wrappers
        wrapper_index_html_file = open(TEMPLATES_DIR + "/wrapper_index.html", "r")
        wrapper_index_html = wrapper_index_html_file.read()
        wrapper_index_html_file.close()

        index_html = wrapper_index_html.replace("$(CONTENT)\n", html)

        wrapper_style_css_file = open(TEMPLATES_DIR + "/wrapper_style.css", "r")
        wrapper_style_css = wrapper_style_css_file.read()
        wrapper_style_css_file.close()

        style_css = wrapper_style_css.replace("$(CONTENT)", css.rstrip())

        # write files
        with open(ROOT_DIR + "/index.html", "w") as index_html_file:
            index_html_file.write(index_html)

        with open(ROOT_DIR + "/style.css", "w") as style_css_file:
            style_css_file.write(style_css)

    def get_ip_address(self):
        hostname = socket.gethostname()
        ip_addr = socket.gethostbyname(hostname)
        return ip_addr

    def get_url_for_profile(self, profile_name):
        return "http://" + self.get_ip_address() + ":" + str(PORT) + "/" + self.get_profile_index_html_file(profile_name)
