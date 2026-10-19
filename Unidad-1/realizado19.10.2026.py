import threading

realizado = False

def trabajo():
	global realizado # NO en la pila sino en la mem principal. 
			 # Eso significa el global
			 # Sin el global, la variable seria local

	if not realizado:
		realizado=True # Operacion entrada salida
		print("Lo hice yo")

	      # print("Lo hice yo")
	      # realizado=True
	      # Si lo hiceramos al reves, le 'Lo hice yo' se ejecuta por ambos porque aqui no tenemos la operacion de entrada y salida
	      # que modifica el resultado final hasta despues de el 'print'
		  
t=threading.Thread(target=trabajo,daemon=False)
t.start() # El hilo secundario ejecuta la funcion 'trabajo'
trabajo() # Despues lo ejecuta el principal

# No sabemos con certeza cual se ejecutará primero
# 1ª Manera: Cualquiera lo ejecuta y el segundo no lo hace porque la variable ahora es 'True' y no ejecuta el print
# 2ª Manera: El sistema en culquier momento puede cambiar el contexto a media ejecucion. 
	# LLegas a 'if not realizado' y te saca el sistema y luego entra el otro.
	# Vuelve el primero y ahora ejecuta 'realizado=True' y ejectura el 'print'
	# Ahora vuelve el segundo desde el mismo punto, y ejecuta otra vez el 'realizado=True' ejecutando otra vez el 'print'

# En la primera solo se ejecuta una vez porque a la zsegunda ya la variable es 'True'
# y en la segunda, ambos hilos fueron parados antes de llegar al 'realizado=True' haciendo que cuando vuelvan, ambos ejecuten el 'print'
