import os
import subprocess
import requests
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("server.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def download_file(url, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    filename = os.path.join(dest_folder, url.split('/')[-1])
    response = requests.get(url)

    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        logger.info(f"File downloaded: {filename}")
    else:
        logger.info(f"Failed to download file: {url}")
        response.raise_for_status()

def run_server():
    # Construct the path to server.py
    server_script = os.path.join('app', 'server.py')
    
    # Run server.py with the 'serve' argument and unbuffered output
    result = subprocess.run(['python3', '-u', server_script, 'serve'], capture_output=True, text=True)
    
    # logger.info the output from server.py
    logger.info("stdout:", result.stdout)
    logger.info("stderr:", result.stderr)

if __name__ == "__main__":
    # URL of the file to download
    file_url = "https://therma.blob.core.windows.net/therma/detection_model.pkl"
    
    # Destination folder
    destination_folder = os.path.join('app', 'models')

    # Download the file
    download_file(file_url, destination_folder)

    # Run the server
    run_server()
