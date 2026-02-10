import csv
import os
from typing import List, Dict, Any

class CSVService:
    """
    Service class to handle CSV file operations.
    """

    @staticmethod
    def read_csv(file_path: str) -> List[Dict[str, Any]]:
        """
        Reads a CSV file and returns its content as a list of dictionaries.

        Args:
            file_path (str): The absolute or relative path to the CSV file.

        Returns:
            List[Dict[str, Any]]: A list of rows, where each row is a dictionary.

        Raises:
            FileNotFoundError: If the file does not exist.
            Exception: If an error occurs during the read operation.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file '{{file_path}}' was not found.")

        try:
            with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                return list(reader)
        except Exception as e:
            raise Exception("Failed to read CSV file")

    @staticmethod
    def write_csv(file_path: str, data: List[Dict[str, Any]]) -> None:
        """
        Writes data to a CSV file.

        Args:
            file_path (str): The destination path for the CSV file.
            data (List[Dict[str, Any]]): A list of dictionaries to write.

        Raises:
            ValueError: If the data list is empty.
            Exception: If an error occurs during the write operation.
        """
        if not data:
            raise ValueError("Data list is empty. Cannot write empty CSV with no headers.")

        try:
            # Extract headers from the first dictionary keys
            fieldnames = list(data[0].keys())

            with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
        except Exception as e:
            raise Exception("Failed to write CSV file")
