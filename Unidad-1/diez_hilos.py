import threading

def hilo():
	print(f"{threading.current_thread().name}") # Imprime cada hilo cuando se ejecute. Similaer a getpid()
def entrada():
	dato=input("Dame el dato") # Lee el teclado y se para el main thread
			   # Hasta que no pongamos un input no continuara el resto del programa	

hilos=[]
t=threading.Thread(target=entrada)
t.start()
# Con esta forma, todos los hilos terminan y el proceso se queda esperando al final a que pongamos la entrada en teclado
# Esto hacia que si abriamos otra terminal, el proceso se veia como activo porque no habia terminado todavia.

print(f"{threading.current_thread().name}")

for i in range(10): # For que con cada iteracion crea un nuevo hilo
	t=threading.Thread(target=hilo)
	hilos.append(t)

for i in hilos:
	i.start() # Llamara a la funcion hilo, para ejecutar el print de su nombre
	          # Igual a hacer 'print(i.name)' -> Que imprimira los nombres de los hilos 1 -> 10
