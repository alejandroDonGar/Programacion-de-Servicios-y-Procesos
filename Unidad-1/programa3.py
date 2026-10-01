import os,time,sys

pid = os.fork() # Se clona el proceso: a partir de aquí hay padre e hijo

if pid == 0:
	#Hijo
	print(f"PID: {os.getpid()}")
	nombre = input("Ingrese su nombre: ") # El hijo comparte la terminal con el padre (se hereda con el fork)
	time.sleep(5)
	print(f"El proceso hijo va a terminar. Has escrito {nombre}")
	sys.exit(5) # Termina el hijo con código de salida 5 (0 = todo bien, otro número = error)
else:
	#Padre
	pid,status = os.wait() # El padre se bloquea hasta que termine el hijo. Devuelve el PID del hijo y su estado codificado
	codigo = os.waitstatus_to_exitcode(status) # Descodifica el estado: 1280 -> 5 (el número que puso el hijo en sys.exit)
	print(f"Soy el Padre con PID: {os.getpid()}. EL hijo ha terminado con PID: {pid} y estado: {codigo}")
