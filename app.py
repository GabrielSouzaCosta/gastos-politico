from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


options = webdriver.ChromeOptions() 
options.add_argument("headless")

class Robo:
    def __init__(self):
        self.driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))
        self.obter_gastos()
        self.driver.quit()

    def obter_gastos(self):
        data = []
        while True:
            politico = input('Politíco a ser analisado (digite "s" para sair): ')
            if politico == 's':
                df = pd.DataFrame.from_dict(d for d in data)
                df.fillna(value = "R$ 0,00", inplace = True)
                print(df.head())
                df.to_csv('gastos.csv')
                break
            
            while True:
                ano = input('Ano a ser analisado [2022, 2021, 2020, 2019]: ')
                if ano in ['2022', '2021', '2020', '2019']:
                    break

            print('buscando dados...')
            self.driver.get("https://www.camara.leg.br/transparencia/gastos-parlamentares?ano="+ano)
            self.driver.implicitly_wait(10)

            search_politico_input = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/main/section[1]/div[1]/div[2]/div/div/div/form/div[1]/div/div[2]/div[2]/div[2]/span[1]/input")
            search_politico_input.click()
            search_politico_input.send_keys(politico)
            sleep(0.5)
            search_politico_input.send_keys(Keys.ARROW_DOWN + Keys.ENTER + Keys.ENTER)
            sleep(0.5)
            self.driver.find_element(By.XPATH, '//*[@id="cota"]/div/div[3]/button').click()
            sleep(0.5)

            nome = self.driver.find_element(By.XPATH, '//*[@id="conteudo-tabela-comparativa"]/li/article/header/dl/dd[1]').text
            partido = self.driver.find_element(By.XPATH, '//*[@id="conteudo-tabela-comparativa"]/li/article/header/dl/dd[2]').text
            estado = self.driver.find_element(By.XPATH, '//*[@id="conteudo-tabela-comparativa"]/li/article/header/dl/dd[3]').text.split('-')[1].strip(' ')
            total = self.driver.find_element(By.XPATH, '//*[@id="conteudo-tabela-comparativa"]/li/article/header/dl/dd[4]').text
            tipo_gasto = self.driver.find_elements(By.XPATH, '//*[@id="conteudo-tabela-comparativa"]/li/article/section/dl/dt/span')
            valor = self.driver.find_elements(By.XPATH, '//*[@id="conteudo-tabela-comparativa"]/li/article/section/dl/dd/span')

            item = self.showData(nome=nome, partido=partido, estado=estado, total=total, tipo_gasto=tipo_gasto, valor=valor, ano=ano)

            if item['Nome'] not in (d['Nome'] for d in data):
                data.append(item)

    def showData(self, *args, **kwargs):
        data = {}
        print(f"\n{kwargs.get('nome')} - {kwargs.get('partido')}/{kwargs.get('estado')} {kwargs.get('ano')}")
        print('-'*75)
        print(f'{"Tipo de gasto":<51}{"Valor Gasto":<15}')
        data['Nome'] = kwargs.get('nome')
        for t, v in zip(kwargs.get('tipo_gasto'), kwargs.get('valor')):
            data[t.text] = v.text
            print(f'{t.text:<50} {v.text:<15}')
        data['Total'] = kwargs.get('total')
        data['Ano'] = kwargs.get('ano')
        print('-'*75)
        print('Total: ' + kwargs.get('total') + '\n')
        return data
            
            
if "__main__" == __name__:
    analisador = Robo()    
    
  
