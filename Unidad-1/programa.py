import os

print("Esto solo lo puede ejecutar el padre") #Aquí solo tenemos el proceso padre

pid = os.fork() # Aqui con fork ya dividimos en dos procesos, padre e hijo)


if pid == 0:
	print(f"El PID del hijo es: {os.getpid()}") # Imprime el PID del hijo porque simpre es 0
else:
	print(f"EL PID del padre es: {os.getpid()}") # Imprime el del padre
	print(f"Y el de mi padre es: {os.getppid()}")
