import pandas as pd
import os

def csv_to_xlsx(csv_folder):
    # Cria uma pasta para salvar os arquivos convertidos se não existir
    output_folder = os.path.join(csv_folder, 'arquivosConvertidos')
    os.makedirs(output_folder, exist_ok=True)
    
    # Lista todos os arquivos CSV na pasta especificada
    for file_name in os.listdir(csv_folder):
        if file_name.endswith('.csv'):
            csv_file_path = os.path.join(csv_folder, file_name)
            
            # Lê o arquivo CSV
            df = pd.read_csv(csv_file_path)
            
            # Constrói o nome de saída para o arquivo XLSX
            xlsx_file_name = os.path.splitext(file_name)[0] + '.xlsx'
            xlsx_file_path = os.path.join(output_folder, xlsx_file_name)
            
            # Salva o dataframe como arquivo XLSX
            df.to_excel(xlsx_file_path, index=False)
            print(f"Arquivo {file_name} convertido para {xlsx_file_name}")
    
    print(f"Todos os arquivos CSV foram convertidos e salvos em '{output_folder}'.")

# Exemplo de uso
csv_folder = "./arquivosParaConversao"  # Substitua pelo caminho da sua pasta com os arquivos CSV
csv_to_xlsx(csv_folder)

