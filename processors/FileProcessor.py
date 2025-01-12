from database import MariaDBHandler

class FileProcessor:
    def __init__(self, db_handler: MariaDBHandler):
        self.db_handler = db_handler

    def process_file(self, file_path: str):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                for line in file:
                    # Divide os campos pelo delimitador "|"
                    data = line.strip().split("|")
                    
                    # Lista de colunas esperadas na tabela
                    columns = ["col1", "col2", "col3"]
                    
                    # Preenche valores faltantes com None
                    while len(data) < len(columns):
                        data.append(None)
                    
                    # Trunca se houver mais valores que colunas
                    if len(data) > len(columns):
                        data = data[:len(columns)]
                    
                    # Insere no banco de dados
                    self.db_handler.insert(
                        table=self.db_handler.getTable(),
                        columns=columns,
                        values=data
                    )
            print(f"Arquivo {file_path} processado com sucesso.")
        except Exception as e:
            print(f"Erro ao processar o arquivo {file_path}: {e}")
