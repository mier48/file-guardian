import os
import hashlib
from collections import defaultdict

class DuplicateChecker:
    @staticmethod
    def get_file_hash(file_path, chunk_size=1024):
        """Calcula el hash MD5 de un archivo."""
        hasher = hashlib.md5()
        with open(file_path, "rb") as file:
            while chunk := file.read(chunk_size):
                hasher.update(chunk)
        return hasher.hexdigest()

    @staticmethod
    def find_duplicates(folder):
        """Encuentra archivos duplicados en una carpeta."""
        hash_map = defaultdict(list)

        for root, _, files in os.walk(folder):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                file_hash = DuplicateChecker.get_file_hash(file_path)
                hash_map[file_hash].append(file_path)

        return {h: paths for h, paths in hash_map.items() if len(paths) > 1}
