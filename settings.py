import csv
import json


class UserSettings(object):
    @staticmethod
    def save_settings(new_settings):
        f = open('settings.csv', "wb")
        w = csv.writer(f)
        for key, val in new_settings.items():
            w.writerow([key, val])
        f.close()

    @staticmethod
    def read_settings():
        f = open('settings.csv', 'rb')
        settings_dict = {}
        for key, val in csv.reader(f):
            settings_dict[key] = val
        f.close()
        return settings_dict

    @staticmethod
    def read_json_settings(key=""):
        try:
            file_vals = json.load(open('settings.json', 'r'))
            if not key:
                return  file_vals

            if file_vals[key]:
                return file_vals[key]

            return file_vals
        except (IOError, KeyError) as err:
            print('Error while reading json file data:',err)
            return {}


    @staticmethod
    def save_json_settings(settings, key):
        file_vals = UserSettings.read_json_settings()
        if (not file_vals):
            file_vals = {}
        file_vals[key] = settings
        res = json.dump(file_vals, open("settings.json", "w"))
        return res
