from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from difflib import SequenceMatcher
from pathlib import Path
import glob
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os
import random
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from seleniumbase import SB


chrome_options = webdriver.ChromeOptions()
download_dir = os.path.abspath('./audiosTnu')
os.makedirs(download_dir, exist_ok=True)
prefs = {'download.default_directory' : download_dir}
chrome_options.add_experimental_option('prefs', prefs)


chromedriver_path = os.path.abspath("chromedriver-linux64/chromedriver")

servico = Service(executable_path=chromedriver_path)

chromium_path = "./chrome-linux64/chrome"   # Replace with the actual path

# Set up Chrome options
chrome_options.add_argument("--headless=new")
chrome_options.binary_location = chromium_path

navegador = webdriver.Chrome(service=servico, options=chrome_options)

navegador.get("https://www.cjf.jus.br/jurisprudencia/tnu/")

#Usando o selenium para clicar no botão pesquisa avançada

navegador.find_element('xpath', '//*[@id="formulario:ckbAvancada"]/div[2]/span').click()

#Usando time para fazer o Selenium esperar carregar página do navegador

time.sleep(1)

# #Clicando e preenchendo o fomulário com as datas que queremos

navegador.find_element('xpath', '//*[@id="formulario:j_idt25_input"]').send_keys("01/12/2022")

navegador.find_element('xpath', '//*[@id="formulario:j_idt27_input"]').send_keys("20/12/2022")

#Clicando no botão enviar, para efetuar a pesquisas

navegador.find_element('xpath', '//*[@id="formulario:actPesquisar"]/span').click()

time.sleep(5)

soup = BeautifulSoup(navegador.page_source, "html.parser")

#Criando a lista de links do interior teor dos acordãos que queremos

linksInteriorTeor = []

links = soup.findAll('a', attrs = {'target' : '_blank'})

for link in links:
    linksInteriorTeor.append(link['href'])
    print(link)

#Abrindo o site da TNU para pegar o áudio do Captch 

numberOfLinks = len(linksInteriorTeor)

counter = 0

while True:
    try:
        navegador.find_element('xpath', '//*[@id=\"formulario:tabelaDocumentos_paginator_top\"]/a[3]/span').click()
        time.sleep(5)
        soup = BeautifulSoup(navegador.page_source, "html.parser")
        links = soup.findAll('a', attrs = {'target' : '_blank'})
        for link in links:
            linksInteriorTeor.append(link['href'])
            print(link)
    except Exception as e:
        print("Erro: ", e)
        break

time.sleep(5)
        
link_remover = 'http://www.cjf.jus.br/'
# Remova o link da lista
linksFiltrados = [link for link in linksInteriorTeor if link != link_remover]

numeroLinks = len(linksFiltrados)

time.sleep(5)

while(counter != numeroLinks):
    with SB(uc=True, test=True, xvfb=True) as sb:
        url = linksFiltrados[counter]
        
        # Abre a página e tenta reconectar até 4 vezes, se necessário
        sb.uc_open_with_reconnect(url, 4)
        
        # Clique no captcha (se necessário)
        sb.uc_gui_click_captcha()
        
        # Agora, clica no botão com o ID 'sbmConsultar'
        sb.click('#sbmConsultar')  # Clica no botão com o ID sbmConsultar

        time.sleep(4)

        time.sleep(4)

        soup = BeautifulSoup(sb.driver.page_source, "html.parser")

        time.sleep(5)

        #html_save_path = fr'request\htmlInteriorTeor\teste{counter}.html'

        directory = './htmlInteriorTeor'

        # Cria o diretório se ele não existir
        os.makedirs(directory, exist_ok=True)

        # Caminho completo para salvar o arquivo HTML
        html_save_path = fr'{directory}/popo{counter}.html'    

        with open(html_save_path, 'wt', encoding='utf-8') as html_file:
            for line in soup.prettify():
                html_file.write(line)

        time.sleep(5)

        counter = counter + 1

# while(counter != numeroLinks):

#     navegador.get(linksFiltrados[counter])

#     navegador.find_element('xpath', '//*[@id="infraImgAudioCaptcha"]').click()

#     time.sleep(1)

#     somElementoInteiro = navegador.find_element('xpath', '//*[@id="infraSrcAudioCaptcha"]')
#     somSourceLink = somElementoInteiro.get_attribute("src")
#     print(somSourceLink)

#     navegador.execute_script("window.open('about:blank', 'secondtab');")
#     navegador.switch_to.window("secondtab")

#     navegador.get(somSourceLink)

#     time.sleep(1)

#     navegador.maximize_window()

#     time.sleep(1)

#     el= navegador.find_element('xpath', '/html/body/video')

#     navegador.find_element(By.TAG_NAME, 'video').click()

#     action = ActionBuilder(navegador)
#     action.pointer_action.move_to_location(775, 300)
#     action.pointer_action.click()
#     action.perform()

#     time.sleep(1)

#     action = ActionChains(navegador)
#     action.send_keys(Keys.TAB)
#     action.send_keys(Keys.TAB)
#     action.send_keys(Keys.TAB)
#     action.send_keys(Keys.TAB)
#     action.send_keys(Keys.TAB)

#     action.perform()

#     time.sleep(2)

#     action.send_keys(Keys.ENTER)
#     action.perform()

#     time.sleep(1)

#     action.send_keys(Keys.ENTER)
#     action.perform()

#     time.sleep(1)

#     tempo_espera = random.uniform(1, 5)

#     time.sleep(tempo_espera)

#     #Partindo o áudio do Captcha com base no silêncio

#     sound = AudioSegment.from_file('./audiosTnu/infra_gerar_audio_captcha.wav', format="wav")
#     audio_chunks = split_on_silence(sound, min_silence_len=500, silence_thresh=-50)
#     for i, chunk in enumerate(audio_chunks):
#         output_file = "audiosTnu/chunk{0}.wav".format(i)
#         chunk.export(output_file, format="wav")

#     # Descobrindo as letras/números do Captcha

#     dir_path = os.path.abspath(r"./alfabetoNumeros/*.*")
#     res = glob.glob(dir_path)

#     threshold = 0.8

#     CaptchCode = (str(CompararAudios(r'audiosTnu/chunk0.wav', res)) + str(CompararAudios(r'audiosTnu/chunk1.wav', res)) + str(CompararAudios(r'audiosTnu/chunk2.wav', res)) + str(CompararAudios(r'audiosTnu/chunk3.wav', res)))

#     time.sleep(5)

#     navegador.switch_to.window(navegador.window_handles[0])

#     navegador.find_element('xpath', '//*[@id="txtInfraCaptcha"]').send_keys(CaptchCode)

#     navegador.find_element('xpath', '//*[@id="sbmConsultar"]').click()

#     tempo_espera2 = random.uniform(1, 10)

#     time.sleep(tempo_espera2)

#     soup = BeautifulSoup(navegador.page_source, "html.parser")

#     time.sleep(tempo_espera2)

#     #html_save_path = fr'request\htmlInteriorTeor\teste{counter}.html'

#     directory = './htmlInteriorTeor'

#     # Cria o diretório se ele não existir
#     os.makedirs(directory, exist_ok=True)

#     # Caminho completo para salvar o arquivo HTML
#     html_save_path = fr'{directory}/InteriorTeor{counter}.html'    

#     with open(html_save_path, 'wt', encoding='utf-8') as html_file:
#         for line in soup.prettify():
#             html_file.write(line)

#     os.remove(r"audiosTnu/infra_gerar_audio_captcha.wav")
#     os.remove(r"audiosTnu/chunk0.wav")
#     os.remove(r"audiosTnu/chunk1.wav")
#     os.remove(r"audiosTnu/chunk2.wav")
#     os.remove(r"audiosTnu/chunk3.wav")
    
#     counter = counter + 1

print("ACABOU!!!!")