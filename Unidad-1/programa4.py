import os

pid = os.fork()
a = pid + 5 # Aqué se ejecutan los dos, PID padre y PID hijo + 5

print(f"Soy PID = ${os.getpid()} y a = ${a}")
