import threading,time

def Saludando():
	# time.sleep(1) <- Si lo ponemos aquí se eejcutará el main primero y luego el secundario
	print("Hola, soy el hilo secundario")

print("Soy el Main Thread o Hilo Principal")

# Creamos un objeto Thread asignandole un target apuntando a la funcion.
# Ahora si se crea un hilo que apunta a la función en concreto.
t = threading.Thread(target = Saludando)

t.start() # Ejecuta el metodo. Ya se puede lanzar el dado.
	  # Despues del 'start' puede o no ejecutarse en orden el hilo, depende de cuando le de quantum el SO.

#time.sleep(1) <- Si lo ponemos aquí el SO saca el hilo principal.
print("Soy el Main Thread o Hilo Principal despues")


# Explicar como funciona en base a la explicacion del readme.
