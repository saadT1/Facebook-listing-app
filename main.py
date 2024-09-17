import subprocess

# Docker command to run the container
docker_command = "docker run -d -p 32768:4444 --name test selenium/standalone-chrome:latest"

# Execute the command using subprocess
try:
    result = subprocess.run(docker_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Container started successfully.")
    print(result.stdout.decode())  # Output from the command
except subprocess.CalledProcessError as e:
    print("Error occurred while starting the container.")
    print(e.stderr.decode())  # Error message
