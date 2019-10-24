from src.context import *
from src.model.Serie_data import Serie

conf_path = "./"
json_name = "config.json"


def get_out_path():
    conf = load_config()
    if conf:
        return conf["outpath"]


def get_dwn_link():
    conf = load_config()
    if conf:
        return conf["watchseries_link"]


def get_done_cmd():
    conf = load_config()
    if conf:
        return conf["done_command"]


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


def search_episodes(linkpart, sno):
    res = []
    link = get_dwn_link()+"serie/"+linkpart
    page = requests.get(link).text
    epis = BeautifulSoup(page, 'html.parser')
    seasons = epis.find_all("div", itemprop="season")
    for sea in seasons:
        season_link = sea.find("a")["href"]
        s_no = int(season_link[season_link.find("season-"):][7:])
        if sno == s_no:
            episodes = sea.find_all("li")
            for e in episodes:
                e_no = e.find("meta")["content"]
                e_link = e.find("a")["href"]
                res.append((e_no, e_link))
        else:
            continue
    return res
