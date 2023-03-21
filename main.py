#!C:/Users/AlanNunesdeCastro/PycharmProjects/RPAs_Pweb/venv/Scripts/Python.exe

from consultas import lote_conta
from multiprocessing import Pool
from utils import sub_routines as sbr
import pandas as pd
from typing import List, Any


def main(instancia: int, batch_list: List[Any]):
    r = lote_conta.Routine()
    #  r.nav_and_download_docs(instancia)
    r.guia_valor_info(instancia, batch_list)


def get_batch():
    exl = pd.read_excel("C:\\temp\\data.xlsx", sheet_name=1, header=2)
    lst = exl["guia_recurso"].tolist()
    batch_lst = sbr.split_list_sublists(lst, num_parts=6)

    return batch_lst


if __name__ == "__main__":
    batch = get_batch()
    pool = Pool(processes=6)
    p1 = pool.apply_async(main, [1, batch[0]])
    """p2 = pool.apply_async(main, [2, batch[1]])
    p3 = pool.apply_async(main, [3, batch[2]])
    p4 = pool.apply_async(main, [4, batch[3]])
    p5 = pool.apply_async(main, [5, batch[4]])
    p6 = pool.apply_async(main, [6, batch[5]])"""

    pool.close()
    pool.join()

