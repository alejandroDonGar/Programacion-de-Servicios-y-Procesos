import threading,queue,time

q=queue.Queue(10)
semaforo=threading.Semaphore(10)

def productor():
	global q,semaforo
	while True:
		semaforo.acquire()
		q.put(threading.current_thread().name)

def consumidor():
	global q,semaforo
	while True:
		print(q.get())
		semaforo.release()
		time.sleep(1)

for i in range(10):
	q.put(i)

for i in range(10):
	print(q.get())

# Explicar el codigo y que es el queue
