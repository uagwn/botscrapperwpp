from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import csv
import time
import re
import os


def coleta(driver, num_scrolls, wait_time):
    all_matches = []

    for i in range(num_scrolls):
        page_source = driver.page_source

        matches = re.findall(r'\+55[\d\s\(\)-]+', page_source)
        all_matches.extend(matches)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(wait_time)  # Espera para o carregamento

        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(wait_time)

    return all_matches


def main():
    # Caminho para o ChromeDriver
    chrome_driver_path = r'D:\downloads\chromedriver.exe'  # Atualize para o caminho do seu ChromeDriver

    # Configurações do Chrome
    options = Options()
    temp_profile_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "temp_profile")
    options.add_argument(f'--user-data-dir={temp_profile_dir}')

    # Inicializa o ChromeDriver
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get('https://web.whatsapp.com/')
        print("Página inicial aberta. Navegue manualmente até a página desejada.")

        input("Pressione Enter após ter navegado manualmente para a página desejada...")

        num_scrolls = 5
        wait_time = 2

        all_matches = coleta(driver, num_scrolls, wait_time)

        # Remover duplicatas
        unique_matches = list(set(all_matches))

        # Exibe os resultados encontrados
        if unique_matches:
            print("Números encontrados que começam com +55:")
            for match in unique_matches:
                print(match)

            # Exporta os resultados para um arquivo CSV
            csv_file_path = 'numeros_com_55.csv'
            with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Número'])
                for match in unique_matches:
                    writer.writerow([match])

            print(f"Dados exportados para {csv_file_path}.")
        else:
            print("Nenhum número com +55 encontrado.")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()