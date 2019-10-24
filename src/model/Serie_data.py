

class Serie:
     def __init__(self, s_no, epis, name):
        self.s_no = s_no
        self.epis = epis
        self.name = name


class Episode:
    def __init__(self, serie, e_no, link):
        self.serie = serie
        self.e_no = e_no
        self.link = link