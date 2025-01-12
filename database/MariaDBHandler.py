import os
import mysql.connector
from dotenv import load_dotenv
import sys
from database.DBOperations import DBOperations

# Carregar variáveis do .env
load_dotenv()

class MariaDBHandler(DBOperations):
    def __init__(self):
        self.isOpen = False
        self.table_name = os.getenv("DB_TABLE")

        try:
            self.connection = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME"),
                port=os.getenv("DB_PORT")
            )
            self.cursor = self.connection.cursor()
            self.isOpen = True
            print("Conexão com o banco de dados estabelecida.")

            # Verificar e criar a tabela, se necessário
            self._ensure_table_exists()
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            sys.exit(1)


    def _ensure_table_exists(self):
        """
        Verifica se a tabela existe no banco de dados. Se não existir, cria.
        """
        try:
            query = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                col1 VARCHAR(255),
                col2 VARCHAR(255),
                col3 VARCHAR(255)
            );
            """
            self.cursor.execute(query)
            self.connection.commit()
            print(f"Tabela '{self.table_name}' verificada/criada com sucesso.")
        except Exception as e:
            print(f"Erro ao verificar/criar a tabela '{self.table_name}': {e}")

    def insert(self, table: str, columns: list, values: list):
        if not self.isOpen:
            print("Conexão com o banco de dados não está aberta.")
            return

        try:
            placeholders = ", ".join(["%s"] * len(values))
            columns_str = ", ".join(columns)
            query = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"
            self.cursor.execute(query, values)
            self.connection.commit()
            print(f"Dados inseridos na tabela '{table}'.")
        except Exception as e:
            print(f"Erro ao inserir dados na tabela '{table}': {e}")

    def delete(self, table: str, condition: str):
        if not self.isOpen:
            print("Conexão com o banco de dados não está aberta.")
            return

        try:
            query = f"DELETE FROM {table} WHERE {condition}"
            self.cursor.execute(query)
            self.connection.commit()
            print(f"Dados deletados da tabela '{table}'.")
        except Exception as e:
            print(f"Erro ao deletar dados da tabela '{table}': {e}")

    def update(self, table: str, set_values: dict, condition: str):
        if not self.isOpen:
            print("Conexão com o banco de dados não está aberta.")
            return

        try:
            set_str = ", ".join([f"{col} = %s" for col in set_values.keys()])
            query = f"UPDATE {table} SET {set_str} WHERE {condition}"
            self.cursor.execute(query, list(set_values.values()))
            self.connection.commit()
            print(f"Dados atualizados na tabela '{table}'.")
        except Exception as e:
            print(f"Erro ao atualizar dados na tabela '{table}': {e}")

    def select(self, table: str, columns: list, condition: str = None):
        if not self.isOpen:
            print("Conexão com o banco de dados não está aberta.")
            return

        try:
            columns_str = ", ".join(columns)
            query = f"SELECT {columns_str} FROM {table}"
            if condition:
                query += f" WHERE {condition}"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Erro ao selecionar dados da tabela '{table}': {e}")

    def getTable(self):
        return self.table_name

    def close(self):
        if self.isOpen:
            self.cursor.close()
            self.connection.close()
            self.isOpen = False
            print("Conexão com o banco de dados encerrada.")
