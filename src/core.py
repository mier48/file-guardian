import os
import shutil

class FileOrganizer:
    def __init__(self):
        self.rules = {}

    def load_rules(self, rules_path):
        """Carga las reglas desde un archivo JSON."""
        import json
        with open(rules_path, "r") as file:
            self.rules = json.load(file)

    def organize_file(self, file_path):
        """Organiza un archivo según las reglas configuradas."""
        file_name = os.path.basename(file_path)
        source_folder = os.path.dirname(file_path)

        for folder, extensions in self.rules.items():
            if file_name.lower().endswith(tuple(extensions)):
                dest_path = os.path.join(source_folder, folder)
                os.makedirs(dest_path, exist_ok=True)
                shutil.move(file_path, dest_path)
                return f"{file_name} -> {folder}"

        # Si no coincide con ninguna regla
        other_folder = os.path.join(source_folder, "Otros")
        os.makedirs(other_folder, exist_ok=True)
        shutil.move(file_path, other_folder)
        return f"{file_name} -> Otros"

    def organize_folder(self, source_folder):
        """Organiza todos los archivos en una carpeta dentro de sus subcarpetas."""
        results = []
        for file_name in os.listdir(source_folder):
            file_path = os.path.join(source_folder, file_name)
            if os.path.isfile(file_path):
                result = self.organize_file(file_path)
                results.append(result)
        return results
