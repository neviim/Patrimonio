import csv

def restructure_csv(input_file, output_file):
    with open(input_file, newline='', encoding='utf-8') as csv_in, \
         open(output_file, 'w', newline='', encoding='utf-8') as csv_out:
        reader = csv.reader(csv_in)
        writer = csv.writer(csv_out)
        
        for row in reader:
            # Se qualquer célula da linha tiver conteúdo não vazio, grava a linha
            if any(cell.strip() for cell in row):
                writer.writerow(row)

if __name__ == "__main__":
    input_path = r".\data\aipf-patrimonio.csv"
    output_path = r".\data\aipf-patrimonio_restructured.csv"
    restructure_csv(input_path, output_path)
    print("Arquivo reestruturado foi criado em:", output_path)
    