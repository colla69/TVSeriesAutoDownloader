from src.context import *


dwn_link = "https://www1.swatchseries.to/serie/{}"


def search_episodes(linkpart, sno):
    res = []
    link = dwn_link.format(linkpart)
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
