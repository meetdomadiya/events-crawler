import socket
import time

def wait_for_service(host, port):
    while True:
        try:
            with socket.create_connection((host, port)):
                return
        except OSError:
            print(f"Waiting for {host}:{port}...")
            time.sleep(1)

# Wait for the PostgreSQL database to be ready
wait_for_service('db', 5432)

# Wait for pgAdmin to be ready
wait_for_service('pgadmin', 80)

# Execute the Python script
import subprocess
subprocess.run(["python", "script.py"])
