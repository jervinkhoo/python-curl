import subprocess

# Command to run the second Python script
command = ['python', 'curl_script.py']

# Open the text file in append mode
with open('output.txt', 'a') as file:
    # Run the command and redirect the output to the text file
    subprocess.run(command, stdout=file, stderr=subprocess.STDOUT)