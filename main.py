from consultas import lote_conta
from multiprocessing import Pool


def main(instancia: int):
    r = lote_conta.Routine()
    r.nav_and_download_docs(instancia)


if __name__ == "__main__":
    pool = Pool(processes=6)
    p1 = pool.apply_async(main, [1])
    p2 = pool.apply_async(main, [2])
    p3 = pool.apply_async(main, [3])
    p4 = pool.apply_async(main, [4])
    p5 = pool.apply_async(main, [5])
    p6 = pool.apply_async(main, [6])

    pool.close()
    pool.join()

