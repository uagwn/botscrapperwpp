import csv
import faker

def generate_random_name():
    fake = faker.Faker()
    return fake.name()

def read_numbers_from_csv(input_csv_file):
    numbers = []
    try:
        with open(input_csv_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Pular cabeçalhos
            for row in reader:
                numbers.append(row[0])  # Supondo que o número esteja na primeira coluna
    except FileNotFoundError:
        print(f"Arquivo {input_csv_file} não encontrado.")
    return numbers

def create_csv_with_numbers_and_names(numbers, csv_file_path):
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Número', 'Nome'])  # Cabeçalhos das colunas

        for number in numbers:
            name = generate_random_name()
            writer.writerow([number, name])

def main():
    # Caminho para o arquivo CSV de entrada e saída
    input_csv_file = 'numeros_com_55.csv'
    output_csv_file = 'numeros_com_nomes.csv'

    # Lê os números do arquivo CSV de entrada
    numbers = read_numbers_from_csv(input_csv_file)

    if numbers:
        # Cria o CSV com números e nomes aleatórios
        create_csv_with_numbers_and_names(numbers, output_csv_file)
        print(f"Dados exportados para {output_csv_file}.")
    else:
        print("Nenhum número encontrado para exportar.")

if __name__ == "__main__":
    main()
