import yaml
import json
from box import Box
import os

class ConfigLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.config = self._load_config()

    def _include_constructor_yaml(self, loader, node):
        """
        Custom constructor to handle the `!include` YAML tag.
        Loads the contents of the specified YAML file and returns it.
        """
        file_name = loader.construct_scalar(node)
        return self._load_included_file(file_name)

    def _include_constructor_json(self, value):
        """
        Custom loader for handling the `!load` directive in JSON files.
        Loads the contents of the specified JSON file and returns it.
        """
        file_name = value.replace('!load ', '').strip()
        return self._load_included_file(file_name)

    def _load_included_file(self, file_name):
        """
        Helper function to load an included file, either YAML or JSON.
        """
        base_path = os.path.dirname(self.file_path)
        full_path = os.path.join(base_path, file_name)

        if full_path.endswith('.yml') or full_path.endswith('.yaml'):
            with open(full_path, 'r') as included_file:
                included_data = yaml.safe_load(included_file)
        elif full_path.endswith('.json'):
            with open(full_path, 'r') as included_file:
                included_data = json.load(included_file)
        else:
            raise ValueError(f"Unsupported file type for included file: {file_name}")

        return included_data

    def _load_config(self):
        """
        Loads the main configuration file (YAML or JSON) and handles `!include` or `!load` tags.
        """
        yaml.SafeLoader.add_constructor('!include', self._include_constructor_yaml)

        if self.file_path.endswith('.yml') or self.file_path.endswith('.yaml'):
            with open(self.file_path, 'r') as file:
                data = yaml.safe_load(file)
        elif self.file_path.endswith('.json'):
            with open(self.file_path, 'r') as file:
                data = json.load(file)

            data = self._process_json_includes(data)
        else:
            raise ValueError("Unsupported file format. Only .yml, .yaml, and .json are supported.")

        return Box(data)

    def _process_json_includes(self, data):
        """
        Recursively processes JSON data to handle `!load` directives.
        """
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str) and value.startswith('!load'):
                    data[key] = self._include_constructor_json(value)
                elif isinstance(value, dict) or isinstance(value, list):
                    data[key] = self._process_json_includes(value)
        elif isinstance(data, list):
            data = [self._process_json_includes(item) for item in data]

        return data

    def get_config(self):
        """
        Returns the loaded configuration as a Box object.
        """
        return self.config
