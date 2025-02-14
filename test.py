import re
import sys
import time
try:
    with open('C:\\Users\\amogh\\Desktop\\xuc\\data.txt', "r") as file:
        for line in file:
            match = re.search(r":\s*(\d+)$", line)  
            if match:
                ecg_value = int(match.group(1)) 
                if ecg_value > 60 or ecg_value < 100:  
                  return 1
        return 0
                
except FileNotFoundError:
         print(f"Error: File '{file_path}' not found.")