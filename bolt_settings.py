import csv


class BoltSettings(object):
    @staticmethod
    def save_dict(dict_rap):
        f = open('bolt_settings.dict', "wb")
        w = csv.writer(f)
        for key, val in dict_rap.items():
            w.writerow([key, val])
        f.close()

    @staticmethod
    def read_dict():
        f = open('bolt_settings.dict', 'rb')
        dict_rap = {}
        for key, val in csv.reader(f):
            dict_rap[key] = val  # eval(val)
        f.close()
        return dict_rap
