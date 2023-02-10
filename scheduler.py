import time
import subprocess

while True:
    # Run script 1
    subprocess.run(["python", "main.py"])

    # Wait for one minute
    time.sleep(60)