import json
import os
import netifaces

from shutil import copyfile

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
                        "profiles": [
                            {
                                "index_html": "index.html",
                                "name": "default",
                                "style_css": "style.css"
                            },
                            {
                                "index_html": "index_miami.html",
                                "name": "miami",
                                "style_css": "style_miami.css"
                            },
                            {
                                "index_html": "index_risingsun.html",
                                "name": "rising sun",
                                "style_css": "style_risingsun.css"
                            },
                            {
                                "index_html": "index_barcode.html",
                                "name": "barcode",
                                "style_css": "style_barcode.css"
                            },
                            {
                                "index_html": "index_commandline.html",
                                "name": "command line",
                                "style_css": "style_commandline.css"
                            }
                        ],
                            "settings": {
                            "temperature_system": "C"
                        }
                    }
                            
                
                    json.dump(self.data, json_file, sort_keys=True, indent=4)

            except Exception as e:
                raise JsonFileCreateException 

        # read config
        else: 
            with open(self.json_path.resolve(), 'r') as json_file:
                self.data = json.load(json_file)

        self.observers = []

        self.temperature_observers = []
        self.temperature = 0

        self.online_status_observers = []
        self.online_status = False

    def register_observer(self, observer):
        self.observers.append(observer)

    def __notify_observers(self):
        for observer in self.observers:
            observer.notify()

    def register_temperature_observer(self, temperature_observer):
        self.temperature_observers.append(temperature_observer)

    def __notify_temperature_observers(self):
        for temperature_observer in self.temperature_observers:
            temperature_observer.update_temperature()

    def register_online_status_observer(self, online_status_observer):
        self.online_status_observers.append(online_status_observer)

    def __notify_online_status_observers(self):
        for online_status_observer in self.online_status_observers:
            online_status_observer.update_online_status()

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

    def __apply_index_html_wrapper(self, index_html_content, profile_name):
        # apply wrappers
        wrapper_index_html_file = open(TEMPLATES_DIR + "/wrapper_index.html", "r")
        wrapper_index_html = wrapper_index_html_file.read()
        wrapper_index_html_file.close()

        index_html = wrapper_index_html.replace("$(CONTENT)\n", index_html_content)

        # replace 'style.css' string with the profile style.css
        index_html = index_html.replace('<link rel="stylesheet" href="style.css" />', '<link rel="stylesheet" href="' + self.get_profile_style_css_file_name(profile_name) + '" />')

        return index_html

    def __apply_style_css_wrapper(self, style_css_content):
        wrapper_style_css_file = open(TEMPLATES_DIR + "/wrapper_style.css", "r")
        wrapper_style_css = wrapper_style_css_file.read()
        wrapper_style_css_file.close()

        style_css = wrapper_style_css.replace("$(CONTENT)", style_css_content.rstrip())

        return style_css

    def __assemble_index_style_template(self, profile_name):
        # read content_index.html 
        index_html_content = open(TEMPLATES_DIR + "/content_index.html", "r")
        index_html_content = index_html_content.read()
        index_html = self.__apply_index_html_wrapper(index_html_content, profile_name)

        style_css_content = open(TEMPLATES_DIR + "/content_style.css", "r")
        style_css_content = style_css_content.read()
        style_css = self.__apply_style_css_wrapper(style_css_content)

        with open(ROOT_DIR + "/" + self.get_profile_index_html_file_name(profile_name), "w") as index_html_file:
            index_html_file.write(index_html)

        with open(ROOT_DIR + "/" + self.get_profile_style_css_file_name(profile_name), "w") as style_css_file:
            style_css_file.write(style_css)

    def __update_temperature_file(self):
        with open(ROOT_DIR + "/" + "temperature.txt", "w") as temperature_file:
            temperature_file.write("{:.0f}".format(self.get_temperature()))

    def get_temperature_system(self):
        return self.data['settings']['temperature_system']

    def set_temperature_system(self, temperature_system):
        if temperature_system == "C" or temperature_system == "F":
            self.data['settings']['temperature_system'] = temperature_system
            self.__update_temperature_file()
            self.__save_json()
            self.__notify_observers()

    def set_temperature(self, temperature):
        self.temperature = temperature

        self.__update_temperature_file()
        self.__notify_temperature_observers()

    def get_temperature(self):
        if self.data['settings']['temperature_system'] == "C":
            return self.temperature
        else:
            return (self.temperature * (9/5)) + 32

    def set_online_status(self, online_status):
        self.online_status = online_status
        self.__notify_online_status_observers()

    def get_profile_names(self):
        profile_names = []     
        for profile in self.data['profiles']:
            profile_names.append(profile['name'])

        sorted_profile_names = sorted(profile_names, key=str.casefold)
        sorted_profile_names.remove('default')
        sorted_profile_names = ['default'] + sorted_profile_names
        return sorted_profile_names


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

        # get file names
        index_html_file_name = 'index_' + self.__name_filter(profile_name) + '.html'
        style_css_file_name = 'style_' + self.__name_filter(profile_name) + '.css'
    
        self.data['profiles'].append({
            'name': profile_name,
            'index_html': index_html_file_name,
            'style_css': style_css_file_name
        })

        self.__assemble_index_style_template(profile_name)

        self.__save_json()
        self.__notify_observers()

    def delete_profile(self, profile_name):
        if profile_name != self.get_default_profile_name():
            new_profiles = []
           
            for profile in self.data['profiles']:
                if profile['name'] != profile_name:
                    new_profiles.append(profile)
                else:
                    os.remove(ROOT_DIR + "/" + profile['index_html'])
                    os.remove(ROOT_DIR + "/" + profile['style_css'])

            self.data['profiles'] = new_profiles

            self.__save_json()
            self.__notify_observers()

    def get_profile_index_html_file_name(self, profile_name):
        for profile in self.data['profiles']:
            if profile_name == profile['name']:
                return profile['index_html']

        return 'index.html'

    def get_profile_style_css_file_name(self, profile_name):
        for profile in self.data['profiles']:
            if profile_name == profile['name']:
                return profile['style_css']

        return 'style.css'


    def get_html(self, profile_name):
        # read root_dir/index.html
        index_html_file = open(ROOT_DIR+ "/" + self.get_profile_index_html_file_name(profile_name), "r")
        index_html = index_html_file.read()
        index_html_file.close()
       
        # replace style css line TODO do with regex
        index_html = index_html.replace('<link rel="stylesheet" href="' + self.get_profile_style_css_file_name(profile_name) + '" />', '<link rel="stylesheet" href="style.css" />')
        
        # remove wrapper
        wrapper_index_html_file = open(TEMPLATES_DIR + "/wrapper_index.html", "r")
        wrapper_index_html = wrapper_index_html_file.read().split("$(CONTENT)")
        wrapper_index_html_file.close()

        wrapper_index_html_top = wrapper_index_html[0]
        wrapper_index_html_bottom = wrapper_index_html[1]

        index_html = index_html.replace(wrapper_index_html_top, '') 
        index_html = index_html.replace(wrapper_index_html_bottom, '') 

        return index_html

    def get_css(self, profile_name):
        # read root_dir/style.css
        style_css_file = open(ROOT_DIR + "/" + self.get_profile_style_css_file_name(profile_name), "r")
        style_css = style_css_file.read()
        style_css_file.close()

        # remove wrapper
        wrapper_style_css_file = open(TEMPLATES_DIR + "/wrapper_style.css", "r")
        wrapper_style_css = wrapper_style_css_file.read().replace("\n$(CONTENT)", "")
        wrapper_style_css_file.close()

        style_css = style_css.replace(wrapper_style_css, "")

        return style_css

    def save_profile(self, profile_name, html, css):
        index_html = self.__apply_index_html_wrapper(html, profile_name)
        style_css = self.__apply_style_css_wrapper(css)

        # write files
        with open(ROOT_DIR + "/" + self.get_profile_index_html_file_name(profile_name), "w") as index_html_file:
            index_html_file.write(index_html)

        with open(ROOT_DIR + "/" + self.get_profile_style_css_file_name(profile_name), "w") as style_css_file:
            style_css_file.write(style_css)


    def reset_profile(self, profile_name):
        self.__assemble_index_style_template(profile_name)
        self.__notify_observers()

    def get_ip_address(self):

        # TODO fix and display multiple addresses in MainWindow
        # get all IPv4 addresses 
        ip_list = []
        for interface in netifaces.interfaces():
            for link in netifaces.ifaddresses(interface).get(netifaces.AF_INET, ()):
                if '127.0' not in link['addr']:
                    ip_list.append(link['addr'])


        if len(ip_list) < 1:
            return "localhost"

        return ip_list[0]

    def get_url_for_profile(self, profile_name):
        return "http://" + self.get_ip_address() + ":" + str(PORT) + "/" + self.get_profile_index_html_file_name(profile_name)

