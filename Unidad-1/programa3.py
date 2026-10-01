import os,time,sys

pid = os.fork()

if pid == 0:
	#Hijo
	print(f"PID: {os.getpid()}")
	nombre = input("Ingrese su nombre: ")
	time.sleep(5)
	print(f"El proceso hijo va a terminar. Has escrito {nombre}")
	sys.exit(5)
else: 
	#Padre
	pid,status = os.wait()
	codigo = os.waitstatus_to_exitcode(status)
	print(f"Soy el Padre con PID: {os.getpid()}. EL hijo ha terminado con PID: {pid} y estado: {codigo}")
