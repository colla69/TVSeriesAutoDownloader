from src.context import *
from src.model.Serie_data import Serie
from src.tools.serie_handler import search_episodes


conf_path = "./"
json_name = "config.json"


def get_out_path():
    conf = load_config()
    if conf:
        return conf["outpath"]


def load_todo_list():
    conf = load_config()
    res = []
    if conf:
        for s in conf["series"]:
            for n in s["no"]:
                sno = n
                sname = s["name"]
                slink = s["linkpart"]
                sepis = search_episodes(slink, sno)
                ser = Serie(sno, sepis, sname)
                res.append(ser)
    return res


def load_config():
    if not os.path.exists(conf_path):
        os.mkdir(conf_path)
    try:
        conf = json_load(conf_path+json_name)
    except Exception as e:
        print(e)
        conf = None
    return conf
