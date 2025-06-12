import pandas as pd
import logging
import platform
import subprocess
from datetime import datetime

logFileName = f"ping_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    filename = logFileName,
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s'
)

def ping_target(address):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    try : 
        result = subprocess.run(["ping", param, "1", address], capture_output= True, text= True, timeout = 5)
        if result.returncode == 0:
            output = result.stdout
            if "time" in output:
                time_part = output.split("time=")[-1].split[0]
            else:
                time_part = "n/a"
            logging.info(f"Target : {address} - Status : Reachable - Response Time : {time_part}")
        else:
            logging.warning(f"Target : {address} - Status : Unreachable")
    except Exception as e:
        logging.error(f"Target: {address} - Status : Error - Message : {str(e)}")
        
def convert_log_to_excel_file(log_file):
    rows = []
    with open(log_file, 'r') as f:
        for line in f : 
            parts = line.strip().split(" - ", 2)
            if len(parts) == 3:
                timestamp , level, message = parts
                rows.append({"timestamp": timestamp, "level": level , "message" : message})
    df = pd.DataFrame(rows)
    excelFileName = log_file.replace(".log" , ".xlsx")
    df.to_excel(excelFileName, index = False)
    print(f"file created : {excelFileName}")

def main():
    targets = [
        "8.8.8.8",
        "google.com",
        "192.168.1.1",
        "invalid.site"
    ]     

    logging.info("script started")
    for target in targets :
        ping_target(target)
    logging.info("script ended")

    convert_log_to_excel_file(logFileName)

if __name__ == "__main__":
    main()