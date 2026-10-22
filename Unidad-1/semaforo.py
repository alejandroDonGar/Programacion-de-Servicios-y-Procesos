import threading,subprocess,time,random

# EL subprocess es bloqueante. Si una parte no se ejecuta, el proceso no continua.

semaforo=threading.Semaphore(2) # Pueden entrar 2 hilos de una vez.
def ping():
	global semaforo
	semaforo.acquire()
	print(threading.current_thread().name, flush=True)
	subprocess.run(["ping","-c","1","8.8.8.8"])
	time.sleep(1)
	semaforo.release()

for i in range(11):
	t=threading.Thread(target=ping)
	t.start()
