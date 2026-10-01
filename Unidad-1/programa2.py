import os,time


pid=os.fork()

if pid == 0:
	#Hijo
	for i in range(10): 
		print(f"Hijo {os.getpid()}. Iteración{i}") # Interacion dice el numero de la vez que se ejecuta el comando, i desde 0 a 9. 
		time.sleep(1) # Añade 1 segundo de espera entre cada iteracion
else:
	#Padre
	for i in range(10):
		print(f"Padre {os.getpid()}. Iteración{i}")
		time.sleep(2)
