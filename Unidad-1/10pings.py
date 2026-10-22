import threading,subprocess

def ping():
	subprocess.run(["ping","-c","1","8.8.8.8"])

for i in range(10):
	t=threading.Thread(target=ping)
	t.start()

# Ahora en vez de ir ping por ping esperando 10 segundos para 10 pings
# mandamos los 10 de una vez.
