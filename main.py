
from database.MariaDBHandler import MariaDBHandler
from processors.FileProcessor import FileProcessor
from watchers.FileWatcher import FileWatcher

def main():
    # Configurar o banco de dados e processador
    db_handler = MariaDBHandler()
    file_processor = FileProcessor(db_handler)

    # Configurar o observador de arquivos
    directory_to_watch = "./files"  # Substitua pelo caminho da pasta
    file_watcher = FileWatcher(directory_to_watch, file_processor)

    try:
        file_watcher.watch()
    except KeyboardInterrupt:
        print("\nFinalizando o observador de arquivos.")
    finally:
        db_handler.close()

if __name__ == "__main__":
    main()
