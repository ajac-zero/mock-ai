import os
import subprocess

command = ["mockai-server"]
RESPONSE_FILE_PATH = "/app/data/responses.json"

# Check if responses.json exists in /app/data
file_exists = os.path.isfile(RESPONSE_FILE_PATH)

if file_exists:
    command.append(RESPONSE_FILE_PATH)

# Run mockai-server
subprocess.run(command)
