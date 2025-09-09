import csv
from typing import List,Dict,Any

class CsvFetcher:
    def __init__(self, file_path:str)->None:
        self.file_path = file_path

    def fetch(self)-> List[Dict[str,Any]]:
        rows: List[Dict[str,Any]] = []
        with open(self.file_path, newline="",encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                rows.append(row)
        return rows