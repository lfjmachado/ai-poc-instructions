import os
import json
from pyspark.sql import SparkSession

def verify_sql_syntax(file_path):
    """
    Verifica a sintaxe de um arquivo SQL usando Spark SQL.
    """
    try:
        spark = SparkSession.builder.master("local").appName("SQLCheck").getOrCreate()
        with open(file_path, 'r') as file:
            sql_query = file.read()
        # Verifica a sintaxe executando um EXPLAIN
        spark.sql(f"EXPLAIN {sql_query}")
        print(f"Sintaxe do arquivo {file_path} está correta.")
    except Exception as e:
        print(f"Erro de sintaxe no arquivo {file_path}: {str(e)}")
        return False
    finally:
        spark.stop()
    return True

def validate_json_file(file_path, required_keys, default_values):
    """
    Valida um arquivo JSON para garantir que as chaves necessárias estejam presentes e preenchidas.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        for key in required_keys:
            if key not in data:
                print(f"Chave ausente: {key} no arquivo {file_path}")
                return False
            if data[key] is None or data[key] == "":
                print(f"Chave {key} no arquivo {file_path} não está preenchida.")
                return False
        print(f"Arquivo JSON {file_path} é válido.")
    except json.JSONDecodeError as e:
        print(f"Erro ao analisar o arquivo {file_path}: {str(e)}")
        return False
    return True

def main():
    # Definir chaves necessárias e valores padrões para os arquivos JSON
    required_keys = ["key1", "key2", "key3"]
    default_values = ["default1", "default2", "default3"]

    # Verificar todos os arquivos SQL
    sql_files = [os.path.join(root, file) 
                 for root, _, files in os.walk(".") 
                 for file in files if file.endswith(".sql")]
    sql_check_results = [verify_sql_syntax(sql_file) for sql_file in sql_files]

    # Verificar todos os arquivos JSON
    json_files = [os.path.join(root, file) 
                  for root, _, files in os.walk(".") 
                  for file in files if file.endswith(".json")]
    json_check_results = [validate_json_file(json_file, required_keys, default_values) for json_file in json_files]

    # Finalizar com erro se alguma verificação falhou
    if not all(sql_check_results) or not all(json_check_results):
        print("Algumas verificações falharam.")
        exit(1)
    else:
        print("Todas as verificações passaram.")

if __name__ == "__main__":
    main()
