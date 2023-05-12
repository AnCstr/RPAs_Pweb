import os
import zipfile
from baserpa import base_selenium
import time
from glob import glob
from getpass import getpass
from typing import List, Any


def login(pweb: base_selenium.NavegadorWeb) -> None:
    """
    Realiza Login em Site Processys
    :return:
    """
    """username = input("Insira Usuario Processys: ")
    pwd = getpass("Informe Senha Processys: ")"""
    """username = "p-Alan.Castro"
    pwd = "Alca0004*"""
    username = "P-filiphe.peixoto"
    pwd = "Liphe2312*"
    pweb.inserir_texto("//input[@id='username']", texto=username)
    pweb.inserir_texto("//input[@id='password']", texto=pwd)
    pweb.send_enter("//input[@id='username']")

    if not validador_login(pweb):
        print("Login Processys Falhou")
        raise ConnectionRefusedError


def validador_login(pweb: base_selenium.NavegadorWeb) -> bool:
    """
    Valida se login Pweb foi bem sucedido. Retorna False caso login falhe.
    :return: True -> Caso Login Sucesso || False -> Login Falhou
    """
    try:
        pweb.clique_xpath("//a[@href='/ProcessUtilisWebService/app/view/movimentoOperacional/home/']")
        return True
    except BaseException:
        return False


def ok_popup(pweb: base_selenium.NavegadorWeb) -> None:
    try:
        if pweb.elemento_existe("//span[text()='Ok']"):
            pweb.clique_xpath(xpath="//span[text()='Ok']")
    except BaseException:
        pass


def pesquisa_conta(pweb: base_selenium.NavegadorWeb, num_conta: int) -> str:
    pweb.duplo_clique_xpath("//input[@id='porLoteConta_btnLimpar']")
    pweb.inserir_texto("//input[@id='porLoteConta_numeroProtocolo']", texto=num_conta)
    pweb.duplo_clique_xpath("//input[@id='porLote_btnBuscarConta']")
    cont = 0

    while True:
        if pweb.elemento_existe("//td[@aria-describedby="
                                "'porLoteConta_grid_numeroGuiaPrestadorFmt']"):
            break
        else:
            time.sleep(0.2)
            pweb.duplo_clique_xpath("//input[@id='porLote_btnBuscarConta']")
            cont += 1
            if cont == 3:
                break

    alerta = pweb.verifica_alerta(xpath="//div[@id='defaultAttention']")
    if alerta != "sem_alerta":
        if str(alerta) != "None":
            return str(alerta)

    ok_popup(pweb)
    return "ok"


def entra_conta(pweb: base_selenium.NavegadorWeb) -> str:
    if pweb.carregou("//td[@aria-describedby='porLoteConta_grid_numeroGuiaPrestadorFmt']"):
        return "n_loc"
    else:
        pweb.duplo_clique_xpath("//td[@aria-describedby='porLoteConta_grid_numeroGuiaPrestadorFmt']")

    ok_popup(pweb)


def reembolso(pweb: base_selenium.NavegadorWeb) -> bool:
    if pweb.elemento_existe("//span[@id='guiaReembolsoAna_prestadorSpan']"):
        status = pweb.retorna_innertext_xpath("//span[@id='guiaReembolsoAna_prestadorSpan']", txt=True)
        status = status.split("(")[-1].replace(")", "").lower()
        if status == "reembolso":
            return True
        else:
            return False
    else:
        return False


def paperless(pweb: base_selenium.NavegadorWeb) -> bool:
    checkbox = pweb.retorna_value_xpath("//input[@id='contentTab-analiseGuiasMedicasTiss3-content_paperLess']")
    if checkbox == "false":
        return False
    else:
        return True


def btn_download(pweb: base_selenium.NavegadorWeb) -> bool:
    pweb.clique_xpath("//input[@id='contentTab-analiseGuiasMedicasTiss3_btnDocumentos']")
    cont = 1
    while not pweb.elemento_existe("//img[@class='markup-imgDownload']"):
        time.sleep(0.1)
        cont += 1
        if cont >= 10:
            return False
    return True


def download_arquivos(pweb: base_selenium.NavegadorWeb) -> bool:
    arquivos = pweb.elementos("//img[@class='markup-imgDownload']")
    for arq in arquivos:
        pweb.clique_xpath("//img[@class='markup-imgDownload']", tipo='elemento', elemento=arq)
        time.sleep(0.3)

    return len(arquivos)


def btn_download_reembolso(pweb: base_selenium.NavegadorWeb) -> bool:
    pweb.clique_xpath("//input[@id='guiaReembolsoAna_btnDocSol']")
    cont = 1
    while not pweb.elemento_existe("//img[@class='markup-imgDownload']"):
        time.sleep(0.1)
        cont += 1
        if cont >= 10:
            return False
    return True


def download_paperless(pweb: base_selenium.NavegadorWeb) -> bool:
    pweb.clique_xpath("//input[@id='contentTab-analiseGuiasMedicasTiss3_btnLst']")
    windows = pweb.driver.window_handles


def renomeia_arquivos(novo_nome: str, folder_path: str) -> int:
    files = glob(f'{folder_path}/*.pdf')
    for idx, file in enumerate(files):
        file_type = file.split(".")[-1]
        new_name = f"{novo_nome}_{idx}.{file_type}"
        os.rename(file, f"{folder_path}/{new_name}")


def zip_files(novo_nome: str, folder_path: str) -> None:
    files = glob(f'{folder_path}/*.pdf')
    path_zip = f"{folder_path}\\zips\\{novo_nome}.zip"
    for file in files:
        arq = file.split("\\")[-1]
        with zipfile.ZipFile(path_zip, 'a') as zipf:
            zipf.write(file, arq, compress_type=zipfile.ZIP_DEFLATED)

        os.remove(file)


def verifica_downloads_finalizados(path: str, num_downloads: int) -> None:
    count = 0
    while True:
        files = glob(f'{path}/*.pdf')
        if len(files) >= num_downloads:
            break
        time.sleep(0.5)
        count += 1
        if count >= 10:
            raise ConnectionRefusedError


def clean_cache(folder: str) -> None:
    files = glob(f'{folder}/*')
    for file in files:
        os.remove(file)


def sessao_expirada(pweb: base_selenium.NavegadorWeb) -> bool:
    for j in range(1, 10):
        pweb.aceita_alerta()

    while True:
        try:
            pweb.navega_url("https://processys.saudepetrobras.com.br/ProcessUtilisWebService"
                            "/app/view/movimentoOperacional/consultas/porLoteConta/")
            login(pweb)
            pweb.navega_url("https://processys.saudepetrobras.com.br/ProcessUtilisWebService"
                            "/app/view/movimentoOperacional/consultas/porLoteConta/")
            return True
        except BaseException:
            pass


def split_list_sublists(lst: List[Any], num_parts: int) -> List[Any]:
    """
    Create a list of lists splited by the number of parts passed
    :param lst: list to split
    :param num_parts: parts that will split
    :return: list of lists, splited
    """
    remainder = float(str(len(lst)/6 % 1)[:4])
    rem_elements = round(remainder * 6)
    rem_list = [lst.pop(n) for n in range(rem_elements)]
    chunk_size = int(len(lst)/num_parts)
    chunks = [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]
    chunks[-1] = chunks[-1] + rem_list

    return chunks

