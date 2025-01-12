import os
import time

class FileWatcher:
    def __init__(self, directory: str, processor):
        self.directory = directory
        self.processor = processor
        self.processed_files = set()

    def watch(self):
        print(f"Observando a pasta: {self.directory}")
        while True:
            files = set(os.listdir(self.directory))
            new_files = files - self.processed_files

            for file in new_files:
                if file.endswith(".txt"):
                    file_path = os.path.join(self.directory, file)
                    self.processor.process_file(file_path)
                    self.processed_files.add(file)

            time.sleep(5)  # Intervalo de verificação
