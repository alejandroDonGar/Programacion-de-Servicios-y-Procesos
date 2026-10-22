import threading,subprocess

evento=threading.Event() # False por defecto


def ping():
	global evento
	evento.wait() # Los hilos pregunta
	subprocess.run(["ping","-c","1","8.8.8.8"])

for i in range(10):
	t=threading.Thread(target=ping)
	t.start()
# Como por defecto es false, los hilos esperan a que el main ejecute esto:
letra=""
while letra!="m":
	letra=input("Dame una m: ")
evento.set() # Cuando terminen, los hilos se podran ejecutar.
