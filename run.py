import sys
from src.config_loader import ConfigLoader

def main():
    if len(sys.argv) != 2:
        print("Usage: python run.py <path_to_config_file>")
        sys.exit(1)

    config_file_path = sys.argv[1]

    config_loader = ConfigLoader(config_file_path)
    config = config_loader.get_config()

    print("Loaded Configuration:")
    print(config)
    print(config.steps)

if __name__ == "__main__":
    main()
