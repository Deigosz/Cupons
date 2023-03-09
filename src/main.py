import streamlit as st
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from utils import DataJson, Utils
import time
import random


class Automacao:
    def __init__(self, config) -> None:
        if not all(key in config for key in ['user', 'pass', 'qtd', 'type', 'value', 'ori', 'dest', 'convenio']):
            raise ValueError(
                'As chaves do dicionário de configuração estão incompletas.')

        self.user = config['user']
        self.password = config['pass']
        self.qtd = config['qtd']
        self.tipo = config['type']
        self.value = config['value']
        self.ori = config['ori']
        self.dest = config['dest']
        self.convenio = config['convenio']


        self.driver = self.options(webdriver)
        self.login(self.driver, self.user, self.password)


        if hasattr(self, 'toWindowCupom') and self.toWindowCupom(driver=self.driver, url=self.convenio):
            self.clicaEmValores(driver=self.driver)
            self.geraCupom(driver=self.driver, qtd=self.qtd, tipo=self.tipo,
                           value=self.value, ori=self.ori, dest=self.dest)
        else:
            self.driver.quit()


    def options(self, webdriver):
        """Função que faz configurações do webdriver

        Args:
            driver (Webdriver): Webdriver

        Returns:
            driver: Retorna o webdriver podendo acessar 
        """

        options = Options()
        # options.add_argument("--headless")
        options.page_load_strategy = 'normal'
        options.add_experimental_option("detach", True)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(service=ChromeService(
            ChromeDriverManager().install()), options=options)
        driver.maximize_window()

        return driver

   
    def login(self, driver, usuario, senha):
        """Função que faz Login no SmartBus. Obs: Está como estático (Usuário fixo).

        Args:
            driver (Webdriver): O seu Webdriver

        Returns:
            driver: Retorna a tela Logado.
        """

        wait = WebDriverWait(driver, 10, poll_frequency=0.5,ignored_exceptions=None)
        driver.get("https://prod-motta-backoffice-smartbus.oreons.com")
        wait.until(lambda d: driver.find_element(By.NAME, "user")).send_keys(str(usuario))
        wait.until(lambda d: driver.find_element(By.NAME, "password")).send_keys(str(senha))
        driver.find_element(By.ID, 'buttonLogin').click()
        time.sleep(2)


    def clicaEmValores(self, driver):
        time.sleep(3)
        wait = WebDriverWait(driver, 120, poll_frequency=5,ignored_exceptions=None)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='tab required'][2]"))).click()


    def geraCupom(self, driver, qtd, tipo, value, ori, dest):
        barra_de_progresso = st.progress(0)
        """
            a.options[0].text == VALOR FIXO
            a.options[1].text == DESCONTO EM PORCENTAGEM
            a.options[2].text == DESCONTO EM VALOR
        """

        for i in range(qtd):

            typeOfCupom = Select(driver.find_element(By.XPATH, '/html/body/smartbuscontroller/smartbusmaster/html/body/div[4]/div/promocode/div/oreonsform/form/div[5]/div/oreonstabs/div[2]/oreonstab[5]/div/promocoderoutevalue/oreonsform/form/div[2]/oreonsdropdownlist/div/div/select'))
            if tipo == 'Desconto em Porcentagem':
                if typeOfCupom.options[1].text == 'DESCONTO EM PORCENTAGEM':

                    if ori != '':
                        Origem = Select(driver.find_element(By.XPATH, '/html/body/smartbuscontroller/smartbusmaster/html/body/div[4]/div/promocode/div/oreonsform/form/div[5]/div/oreonstabs/div[2]/oreonstab[5]/div/promocoderoutevalue/oreonsform/form/div[1]/oreonsdropdownlist[2]/div/div/select'))
                        for option in Origem.options:
                            if option.text == ori:
                                Origem.select_by_visible_text(str(ori))

                    if dest != '':
                        Destino = Select(driver.find_element(By.XPATH, '/html/body/smartbuscontroller/smartbusmaster/html/body/div[4]/div/promocode/div/oreonsform/form/div[5]/div/oreonstabs/div[2]/oreonstab[5]/div/promocoderoutevalue/oreonsform/form/div[1]/oreonsdropdownlist[3]/div/div/select'))
                        for option in Destino.options:
                            if option.text == dest:
                                Destino.select_by_visible_text(str(dest))

                    typeOfCupom.select_by_visible_text('DESCONTO EM PORCENTAGEM')

                    FieldValueOfCupom = driver.find_element(By.XPATH, '/html/body/smartbuscontroller/smartbusmaster/html/body/div[4]/div/promocode/div/oreonsform/form/div[5]/div/oreonstabs/div[2]/oreonstab[5]/div/promocoderoutevalue/oreonsform/form/div[2]/oreonstextbox[3]/div/div/input')
                    driver.execute_script("arguments[0].removeAttribute('disabled')", FieldValueOfCupom)
                    FieldValueOfCupom.send_keys(str(value))  # Porcentagem do Cupom

                    self.NumberOfCupom = self.generatorNumberOfCupom()
                    initClass = DataJson()
                    initClass.salvar_cupom(self.NumberOfCupom)
                    st.write(self.NumberOfCupom)

                    progresso = (i + 1) / qtd
                    barra_de_progresso.progress(progresso, text='Gerando cupons...')

                    Fild_NumberInitial = driver.find_element(By.XPATH, "/html/body/smartbuscontroller/smartbusmaster/html/body/div[4]/div/promocode/div/oreonsform/form/div[5]/div/oreonstabs/div[2]/oreonstab[5]/div/promocoderoutevalue/oreonsform/form/div[4]/oreonstextbox[1]/div/div/input")
                    Fild_NumberFinal = driver.find_element(By.XPATH, "/html/body/smartbuscontroller/smartbusmaster/html/body/div[4]/div/promocode/div/oreonsform/form/div[5]/div/oreonstabs/div[2]/oreonstab[5]/div/promocoderoutevalue/oreonsform/form/div[4]/oreonstextbox[2]/div/div/input")
                    Fild_Qtd = driver.find_element(By.XPATH, "/html/body/smartbuscontroller/smartbusmaster/html/body/div[4]/div/promocode/div/oreonsform/form/div[5]/div/oreonstabs/div[2]/oreonstab[5]/div/promocoderoutevalue/oreonsform/form/div[4]/oreonstextbox[3]/div/div/input")
                    Fild_BtnCommit = driver.find_element(By.XPATH, "/html/body/smartbuscontroller/smartbusmaster/html/body/div[4]/div/promocode/div/oreonsform/form/div[5]/div/oreonstabs/div[2]/oreonstab[5]/div/promocoderoutevalue/oreonsform/form/div[5]/div/oreonsbutton/button")

                    Fild_NumberInitial.send_keys(str(self.NumberOfCupom))
                    Fild_NumberFinal.send_keys(str(self.NumberOfCupom))
                    Fild_Qtd.send_keys(str('01'))
                    Fild_BtnCommit.click()

            elif tipo == 'Desconto em Valor':
                if typeOfCupom.options[2].text == 'DESCONTO EM VALOR':

                    if ori != '':
                        Origem = Select(driver.find_element(By.XPATH, '/html/body/smartbuscontroller/smartbusmaster/html/body/div[4]/div/promocode/div/oreonsform/form/div[5]/div/oreonstabs/div[2]/oreonstab[5]/div/promocoderoutevalue/oreonsform/form/div[1]/oreonsdropdownlist[2]/div/div/select'))
                        for option in Origem.options:
                            if option.text == ori:
                                Origem.select_by_visible_text(str(ori))

                    if dest != '':
                        Destino = Select(driver.find_element(By.XPATH, '/html/body/smartbuscontroller/smartbusmaster/html/body/div[4]/div/promocode/div/oreonsform/form/div[5]/div/oreonstabs/div[2]/oreonstab[5]/div/promocoderoutevalue/oreonsform/form/div[1]/oreonsdropdownlist[3]/div/div/select'))
                        for option in Destino.options:
                            if option.text == dest:
                                Destino.select_by_visible_text(str(dest))

                    typeOfCupom.select_by_visible_text('DESCONTO EM VALOR')

                    FieldValueOfCupom = driver.find_element(By.XPATH, '/html/body/smartbuscontroller/smartbusmaster/html/body/div[4]/div/promocode/div/oreonsform/form/div[5]/div/oreonstabs/div[2]/oreonstab[5]/div/promocoderoutevalue/oreonsform/form/div[2]/oreonstextbox[2]/div/div/input')
                    driver.execute_script("arguments[0].removeAttribute('disabled')", FieldValueOfCupom)
                    FieldValueOfCupom.send_keys(str(value))  # Valor do Cupom

                    self.NumberOfCupom = self.generatorNumberOfCupom()
                    initClass = DataJson()
                    initClass.salvar_cupom(self.NumberOfCupom)
                    st.write(self.NumberOfCupom)

                    progresso = (i + 1) / qtd
                    barra_de_progresso.progress(progresso, text='Gerando cupons...')

                    Fild_NumberInitial = driver.find_element(By.XPATH, "/html/body/smartbuscontroller/smartbusmaster/html/body/div[4]/div/promocode/div/oreonsform/form/div[5]/div/oreonstabs/div[2]/oreonstab[5]/div/promocoderoutevalue/oreonsform/form/div[4]/oreonstextbox[1]/div/div/input")
                    Fild_NumberFinal = driver.find_element(By.XPATH, "/html/body/smartbuscontroller/smartbusmaster/html/body/div[4]/div/promocode/div/oreonsform/form/div[5]/div/oreonstabs/div[2]/oreonstab[5]/div/promocoderoutevalue/oreonsform/form/div[4]/oreonstextbox[2]/div/div/input")
                    Fild_Qtd = driver.find_element(By.XPATH, "/html/body/smartbuscontroller/smartbusmaster/html/body/div[4]/div/promocode/div/oreonsform/form/div[5]/div/oreonstabs/div[2]/oreonstab[5]/div/promocoderoutevalue/oreonsform/form/div[4]/oreonstextbox[3]/div/div/input")
                    Fild_BtnCommit = driver.find_element(By.XPATH, "/html/body/smartbuscontroller/smartbusmaster/html/body/div[4]/div/promocode/div/oreonsform/form/div[5]/div/oreonstabs/div[2]/oreonstab[5]/div/promocoderoutevalue/oreonsform/form/div[5]/div/oreonsbutton/button")

                    Fild_NumberInitial.send_keys(str(self.NumberOfCupom))
                    Fild_NumberFinal.send_keys(str(self.NumberOfCupom))
                    Fild_Qtd.send_keys(str('01'))
                    Fild_BtnCommit.click()

        SaveToOperation = driver.find_element(By.XPATH, '/html/body/smartbuscontroller/smartbusmaster/html/body/div[4]/div/promocode/div/oreonsform/form/div[6]/div[2]/oreonsbutton[1]/button')
        
        if SaveToOperation.text == 'SALVAR':
            SaveToOperation.click()
            st.write('Lote de Cupom Gerado com sucesso!')
            st.balloons()
            time.sleep(5)
            driver.quit()


    def toWindowCupom(self, driver, url):
        """Troca para tela de cupons e espera para tela de cupons ser carregada
        """

        driver.execute_script(f"window.open('{url}')")
        proximaTela = driver.window_handles[1]
        driver.switch_to.window(proximaTela)
        time.sleep(15)
        if 'Código promocional' in driver.title:
            return True
        else:
            return False


    def generatorNumberOfCupom(self):
        numberCupom = random.randint(100000000, 999999999)
        numberCupom = str(numberCupom)
        return numberCupom
    

    def exibeCupom(self, cupons):
        numeros = []
        for i in range(len(cupons)):
            numeros.append(int(cupons[i]))
        # st.write(numeros)


if __name__ == '__main__':
    Automacao()