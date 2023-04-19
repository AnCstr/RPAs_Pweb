import pandas as pd
from utils.sub_routines import split_list_sublists
from os import mkdir
from os.path import isdir


PATH_UNIFICADO = "c:\\temp\\data.xlsx"
PATH_SPLITED = "c:\\temp\\splited_dfs"


class Spliter:
    def __init__(self, partes: int):
        self.__partes = partes

    @staticmethod
    def cria_pasta():
        if not isdir("c:\\temp\\splited_dfs"):
            mkdir("c:\\temp\\splited_dfs")

    def separar(self):
        self.cria_pasta()
        df = pd.read_excel(PATH_UNIFICADO, sheet_name=0)
        lista_guias = df["guia_recurso"].tolist()
        listas_guias = split_list_sublists(lista_guias, self.__partes)
        for idx, lista in enumerate(listas_guias):
            df = pd.DataFrame(data={"guia_recurso": lista})
            df.to_excel(f"{PATH_SPLITED}\\{idx}.xlsx", sheet_name="1")


s = Spliter(2)
s.separar()
