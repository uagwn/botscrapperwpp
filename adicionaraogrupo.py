import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


def read_contacts_from_csv(input_csv_file):
    contacts = []
    try:
        with open(input_csv_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                contacts.append(row[0])
    except FileNotFoundError:
        print(f"Arquivo {input_csv_file} não encontrado.")
    return contacts


def add_contacts_to_group(driver, group_name, contacts):
    # Clica na opção de adicionar participantes
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[5]/span/div/span/div/div/div/section/div[7]/div[2]/div[1]/div[2]/div/div'))
    ).click()
    print("botao add encontrado")

    for contact in contacts:
        # Procura o campo de pesquisa
        search_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div/div[1]/div/div[2]/div[2]/div/div/p'))
        )
        search_box.clear()
        search_box.send_keys(contact)
        time.sleep(3)  # Espera para os resultados da pesquisa carregarem

        # Seleciona o contato
        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, f"//span[@title='{contact}']"))
            ).click()
            search_box.clear()
            print(f"Contato {contact} adicionado com sucesso.")
        except Exception as e:
            search_box.clear()
            print(f"Erro ao adicionar o contato {contact}: {e}")

    # Confirma a adição dos contatos
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div/span[2]/div/div/div'))
    ).click()
    time.sleep(25)

def main():
    # Caminho para o arquivo CSV de contatos
    input_csv_file = 'numeros_com_nomes.csv'

    # Nome do grupo no WhatsApp
    group_name = "Estudos Free #1 - Trade & Ações"  # Substitua pelo nome do grupo

    # Configurações do Chrome
    chrome_driver_path = r'D:\downloads\chromedriver.exe'  # Atualize para o caminho do seu ChromeDriver

    # Configurações do Chrome
    options = Options()
    temp_profile_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "temp_profile")
    options.add_argument(f'--user-data-dir={temp_profile_dir}')

    # Inicializa o ChromeDriver
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Abre o WhatsApp Web
        driver.get('https://web.whatsapp.com/')
        print("WhatsApp Web aberto. Entre manualmente.")

        # Aguardando o usuário para entrar manualmente
        input("Pressione Enter após ter entrado manualmente no WhatsApp Web...")

        # Lê os contatos do arquivo CSV
        contacts = read_contacts_from_csv(input_csv_file)
        contacts = contacts[:50]


        if contacts:
            # Adiciona os contatos ao grupo
            add_contacts_to_group(driver, group_name, contacts)
            print("Contatos adicionados com sucesso!")
        else:
            print("Nenhum contato encontrado para adicionar.")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()