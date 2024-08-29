## Python Config Loader

ConfigLoader is a Python utility class that loads and merges configuration files in both .yml (YAML) and .json formats. It supports custom directives (!include for YAML and !load for JSON) to include additional configuration files dynamically.

#### Features

- Load configuration from .yml (YAML) and .json files.
- Supports !include directive in YAML files to include other YAML files.
- Supports !load directive in JSON files to include other JSON files.
- Provides easy access to configuration using attribute-style access with Box objects.

#### Installation

- Clone the repo
- Install required packages from the requirements.txt file using `pip install -r requirements.txt`

#### Usage

- From the root directory execute the run.py file
- Syntax for executing the run.py file is `python run.py <path_to_config_file>`
- Use the example configs and execute by `python run.py configs/main.yml` or `python run.py configs/main_json.json`
