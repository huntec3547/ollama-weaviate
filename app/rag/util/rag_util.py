import requests 
from bs4 import BeautifulSoup
import re
import json
from pathlib import Path

def donwload_article(source_urls, filepath) -> bool:
    with open(filepath,'w') as f:
        try:
            # Loop throught the source url list
            for url in source_urls:
                response = requests.get(url)
                response.raise_for_status()
                # Parse the response in paragraphs
                soup = BeautifulSoup(response.text, 'html.parser')
                paragraphs = soup.find_all('p', class_=False)
            
                # Write each paragraph to the source file
                for p in paragraphs:
                    line = re.sub(r'[^a-zA-Z0-9 .,:;]\'', '', p.text)
                    f.write(line+'\n')

            return True

        except Exception as e:
            print(f"An error occurred during the request: {e}")
            # Handle network errors, connection issues, etc.
            return False # Or handle the error appropriately
        finally:
            f.close()


def load_config():
    """Loads configuration data from a JSON file."""
    try:
        current_dir = Path.cwd()
        file_path = str(current_dir.absolute())+"/app/config/config.json"
        print(file_path)
        with open(file_path, 'r') as f:
            config_data = json.load(f)
        return config_data
    except FileNotFoundError:
        print(f"Error: Configuration file '{file_path}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{file_path}'.")
        return None  
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None