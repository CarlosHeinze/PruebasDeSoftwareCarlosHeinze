"""
Module to implement a Base Class for Data Saving in the
classes to be implemented by the Hotel System
@author: Carlos Heinze A01700179
"""
import os
import json
from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseClass(ABC):
    """
    Abstract Base Class that allows the classes in the Hotel System to
    inherit and save information to persistent JSON files simulating
    a Data Base that would be used in a real scenario.
    """

    @abstractmethod
    def get_filename(self) -> str:
        """
        Attribute for the Child Classes to add the name of the file to
        save their data. In a real scenario, this could be the name of
        the database table the information is being saved to.
        """

    def load_data(self) -> Dict[str, Any]:
        """
        Loads data from a JSON file to an instance of the class.

        Returns:
            (Dict): A dictionary with the saved information. Empty if the
                    file does not exist or an error occurs.
        """
        filename = self.get_filename()
        if not os.path.exists(filename):
            return {}
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError as error:
            print(f"Error loading {filename}: {error}. "
                  "Continuing with empty data.")
            return {}

    def save_data(self, data: Dict[str, Any]) -> None:
        """
        Saves the information of the instance to a JSON. This meets the
        requiement for persintant data.
        """
        with open(self.get_filename(), 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
