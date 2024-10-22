import pandas as pd
import os

def csv_to_xlsx(csv_folder, chunksize=None):
    # Cria uma pasta para salvar os arquivos convertidos, se não existir
    output_folder = os.path.join(csv_folder, 'arquivosConvertidos')
    os.makedirs(output_folder, exist_ok=True)
    
    # Verifique se a pasta de saída foi criada corretamente
    print(f"Arquivos convertidos serão salvos em: {output_folder}")
    
    # Lista todos os arquivos CSV na pasta especificada
    for file_name in os.listdir(csv_folder):
        if file_name.endswith('.csv'):
            csv_file_path = os.path.join(csv_folder, file_name)
            print(f"Processando o arquivo: {csv_file_path}")
            
            # Função para tentar várias codificações
            def read_csv_with_encoding(path, encoding_list, skiprows=None, nrows=None, usecols=None):
                for encoding in encoding_list:
                    try:
                        return pd.read_csv(path, delimiter=';', encoding=encoding, on_bad_lines='skip', skiprows=skiprows, nrows=nrows, usecols=usecols), encoding
                    except UnicodeDecodeError:
                        print(f"Erro ao ler com a codificação {encoding}, tentando outra...")
                raise UnicodeDecodeError(f"Não foi possível decodificar o arquivo {file_name} com as codificações fornecidas.")
            
            try:
                # Lista de possíveis codificações a tentar
                encodings_to_try = ['utf-8', 'latin1', 'iso-8859-1']

                # Lê as primeiras 7 linhas (da linha 0 até a linha 6) e apenas as duas primeiras colunas
                first_part_df, encoding_used = read_csv_with_encoding(csv_file_path, encodings_to_try, nrows=7, usecols=[0, 1])
                print(f"As primeiras 7 linhas do arquivo {file_name} foram lidas com sucesso (apenas as duas primeiras colunas) usando a codificação {encoding_used}.")

                # Lê da oitava linha até o final (todas as colunas)
                second_part_df, _ = read_csv_with_encoding(csv_file_path, encodings_to_try, skiprows=8)
                print(f"As linhas restantes do arquivo {file_name} foram lidas com sucesso.")

                # Constrói os nomes de saída para os dois arquivos XLSX
                first_part_xlsx_file = os.path.join(output_folder, os.path.splitext(file_name)[0] + '_parte1.xlsx')
                second_part_xlsx_file = os.path.join(output_folder, os.path.splitext(file_name)[0] + '_parte2.xlsx')

                # Salva a primeira parte (linhas 1 a 7, duas primeiras colunas)
                first_part_df.to_excel(first_part_xlsx_file, index=False)
                print(f"As primeiras 7 linhas (duas primeiras colunas) foram salvas em {first_part_xlsx_file}.")

                # Salva a segunda parte (linhas 8 até o final, todas as colunas)
                second_part_df.to_excel(second_part_xlsx_file, index=False)
                print(f"As linhas a partir da 8ª foram salvas em {second_part_xlsx_file}.")
                
            except UnicodeDecodeError as e:
                print(f"Erro ao processar o arquivo {file_name}: {e}")
            except pd.errors.EmptyDataError:
                print(f"Erro: O arquivo {file_name} está vazio ou corrompido.")
            except pd.errors.ParserError as e:
                print(f"Erro ao processar o arquivo {file_name}: Problema ao ler o CSV. Detalhes: {e}")
            except Exception as e:
                print(f"Erro inesperado ao processar o arquivo {file_name}: {e}")
    
    print(f"Todos os arquivos CSV foram processados e salvos em '{output_folder}'.")

# Exemplo de uso
csv_folder = "./arquivosParaConversao"  # Substitua pelo caminho da sua pasta com os arquivos CSV
csv_to_xlsx(csv_folder)
