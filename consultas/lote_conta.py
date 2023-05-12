import pandas as pd
from baserpa import base_selenium as bsl
from utils import sub_routines as sbr
import time
import datetime
from selenium.common.exceptions import UnexpectedAlertPresentException, TimeoutException
from typing import List, Any
import warnings
import os


id_folder = {
    1: "C:\\temp\\kpmg\\anexos",
    2: "C:\\temp\\kpmg\\anexos2",
    3: "C:\\temp\\kpmg\\anexos3",
    4: "C:\\temp\\kpmg\\anexos4",
    5: "C:\\temp\\kpmg\\anexos5",
    6: "C:\\temp\\kpmg\\anexos6",
}


warnings.simplefilter("ignore")


class Routine:
    @staticmethod
    def nav_and_download_docs(instancia: int):
        exl = pd.read_excel(f"C:\\temp\\kpmg\\kpmg{instancia}.xlsx")
        exl = exl.rename(columns={"OK/NOK": "OK", "IDENTIFICAÇÃO_DO_EVENTO": "IDENTIFICACAO_DO_EVENTO"})
        pweb = bsl.NavegadorWeb(url="https://processys.saudepetrobras.com.br/", fldr_id=instancia)
        sbr.login(pweb)
        exl["alertas"] = ""
        paperless = False
        exl["IDENTIFICACAO_DO_EVENTO"] = exl["IDENTIFICACAO_DO_EVENTO"].astype(str)
        for n, conta in enumerate(exl["IDENTIFICACAO_DO_EVENTO"].tolist()):
            start_time = int(time.time())
            try:
                pweb.navega_url("https://processys.saudepetrobras.com.br/ProcessUtilisWebService"
                                "/app/view/movimentoOperacional/consultas/porLoteConta/")

                if conta[-2:] == ".0":
                    conta = conta.replace(".0", "")

                alert = sbr.pesquisa_conta(pweb, conta)
                if alert != "ok":
                    exl["alertas"].loc[n] = alert

                status = sbr.entra_conta(pweb)
                if status == "n_loc":
                    exl["OK"].loc[n] = "n_loc"
                    exl.to_excel(f"c:\\temp\\kpmg\\retorno_kpmg_{instancia}.xlsx", index=False)
                    continue

                reembolso = sbr.reembolso(pweb)

                if not reembolso:
                    paperless = sbr.paperless(pweb)

                #  rotina paperless
                if reembolso:
                    exl["OK"].loc[n] = "reembolso"
                    exl.to_excel(f"c:\\temp\\kpmg\\retorno_kpmg_{instancia}.xlsx", index=False)
                    continue
                elif paperless:
                    exl["OK"].loc[n] = "paperless"
                    exl.to_excel(f"c:\\temp\\kpmg\\retorno_kpmg_{instancia}.xlsx", index=False)
                    continue
                else:
                    sbr.btn_download(pweb)
                    num_files = sbr.download_arquivos(pweb)
                    sbr.verifica_downloads_finalizados(id_folder[instancia], num_files)
                    sbr.renomeia_arquivos(conta, id_folder[instancia])
                    sbr.verifica_downloads_finalizados(id_folder[instancia], num_files)
                    sbr.zip_files(conta, id_folder[instancia])
                    exl["OK"].loc[n] = "Ok"
            except BaseException:
                exl["OK"].loc[n] = "Erro"
                exl.to_excel(f"c:\\temp\\kpmg\\retorno_kpmg_{instancia}.xlsx", index=False)

            exl.to_excel(f"c:\\temp\\kpmg\\retorno_kpmg_{instancia}.xlsx", index=False)
            print(f"Tempo de Execução: {datetime.timedelta(seconds=int(time.time()) - start_time)}")

    @staticmethod
    def guia_valor_info(instancia: int, batch_list: List[Any]):
        exl = pd.DataFrame(data={"guia_recurso": batch_list, "valor_cobrado": "", "valor_pago": ""})
        pweb = bsl.NavegadorWeb(url="https://processys.saudepetrobras.com.br/", fldr_id=instancia)
        sbr.login(pweb)
        pweb.navega_url("https://processys.saudepetrobras.com.br/ProcessUtilisWebService"
                        "/app/view/movimentoOperacional/consultas/porLoteConta/")
        cnt = 0

        for n, conta in enumerate(batch_list):
            os.system("cls")
            start_time = int(time.time())
            print(n)
            conta = int(conta)
            try:
                alert = sbr.pesquisa_conta(pweb, conta)
                if alert != "ok":
                    exl["valor_cobrado"].loc[n] = alert
                    exl.to_excel(f"C:\\temp\\data_{instancia}.xlsx", index=False, float_format="%.2f")

                if pweb.carregou("//td[@aria-describedby='porLoteConta_grid_numeroGuiaPrestadorFmt']"):
                    exl["valor_cobrado"].loc[n] = "N_Loc"
                    exl.to_excel(f"C:\\temp\\data_{instancia}.xlsx", index=False, float_format="%.2f")

                """valor_soli = pweb.retorna_innertext_xpath(
                    "//td[@aria-describedby='porLoteConta_grid_valorInformadoGuia']",
                    txt=True)
                valor_pago = pweb.retorna_innertext_xpath(
                    "//td[@aria-describedby='porLoteConta_grid_valorPagamento']",
                    txt=True)"""
                valor_soli = pweb.retorna_value_xpath(
                    "//input[@id='porLoteConta_quantidadeGuiaLoteInformadoSoma']")
                valor_pago = pweb.retorna_value_xpath(
                    "//input[@id='porLoteConta_totalPago']")

                exl["valor_cobrado"].loc[n] = valor_soli
                exl["valor_pago"].loc[n] = valor_pago

                cnt += 1
                if cnt == 100:
                    exl.to_excel(f"C:\\temp\\data_{instancia}.xlsx", index=False, float_format="%.2f")
                    cnt = 0
                print(f"Tempo de Execução: {datetime.timedelta(seconds=int(time.time()) - start_time)}")
            except UnexpectedAlertPresentException:
                sbr.sessao_expirada(pweb)
                exl["valor_cobrado"].loc[n] = "Erro"
                exl.to_excel(f"C:\\temp\\data_{instancia}.xlsx", index=False, float_format="%.2f")

        exl.to_excel(f"C:\\temp\\data_{instancia}.xlsx", index=False, float_format="%.2f")


    @staticmethod
    def pesquisa_guia_recurso_retorna_data_envio_e_valores(instancia: int, batch_list: List[Any]):
        exl = pd.DataFrame(data={"guia_recurso": batch_list,
                                 "data_envio": "",
                                 "valor_cobrado": "",
                                 "valor_pago": ""
                                 })
        pweb = bsl.NavegadorWeb(url="https://processys.saudepetrobras.com.br/", fldr_id=instancia)
        sbr.login(pweb)
        cnt = 0
        pweb.navega_url("https://processys.saudepetrobras.com.br/ProcessUtilisWebService"
                        "/app/view/movimentoOperacional/consultas/porLoteConta/")

        for n, conta in enumerate(batch_list):
            os.system("cls")
            start_time = int(time.time())
            print(n)
            try:
                alert = sbr.pesquisa_conta(pweb, conta)
                if alert != "ok":
                    exl["data_envio"].loc[n] = alert
                    exl.to_excel(f"C:\\temp\\data_{instancia}.xlsx", index=False, float_format="%.2f")

                if pweb.carregou("//td[@aria-describedby='porLoteConta_grid_numeroGuiaPrestadorFmt']"):
                    exl["data_envio"].loc[n] = "N_Loc"
                    exl.to_excel(f"C:\\temp\\data_{instancia}.xlsx", index=False, float_format="%.2f")

                try:
                    data_envio = pweb.retorna_innertext_xpath(
                        "//td[@aria-describedby='porLoteConta_grid_dataEmissaoGuiaFmt']",
                        txt=True)

                    valor_soli = pweb.retorna_innertext_xpath(
                        "//td[@aria-describedby='porLoteConta_grid_valorInformadoGuia']",
                        txt=True)

                    valor_pago = pweb.retorna_innertext_xpath(
                        "//td[@aria-describedby='porLoteConta_grid_valorPagamento']",
                        txt=True)
                except TimeoutException:
                    exl["data_envio"].loc[n] = "N_Loc"
                    exl.to_excel(f"C:\\temp\\data_{instancia}.xlsx", index=False, float_format="%.2f")
                    continue

                exl["data_envio"].loc[n] = data_envio
                exl["valor_cobrado"].loc[n] = valor_soli
                exl["valor_pago"].loc[n] = valor_pago

                cnt += 1
                if cnt == 1000:
                    exl.to_excel(f"C:\\temp\\data_{instancia}.xlsx", index=False, float_format="%.2f")
                    cnt = 0

                print(f"Tempo de Execução: {datetime.timedelta(seconds=int(time.time()) - start_time)}")
            except UnexpectedAlertPresentException:
                sbr.sessao_expirada(pweb)
                exl["data_envio"].loc[n] = "Erro"
                exl.to_excel(f"C:\\temp\\data_{instancia}.xlsx", index=False, float_format="%.2f")

