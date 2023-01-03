import requests
from pathlib import Path

def main():
    path = str(Path(__file__).parent.parent) + r"\\inputs\\rssi\\yiy7.txt"

    url = 'https://ywsrtls.000webhostapp.com/yiy6.txt'
    r = requests.get(url, allow_redirects=True)

    with open(path, "w") as f:
        fullStr = r.content.decode()
        f.write(fullStr)
        
if __name__ == '__main__':
    main()