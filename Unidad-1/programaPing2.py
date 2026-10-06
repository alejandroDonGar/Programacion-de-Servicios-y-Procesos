import os,subprocess,time,sys

ahora = time.time()

for i in range(10):
	pid = os.fork() # Genera un hijo y el padre vuelve arriba y vuelve a entrar en el bucle hasta hacerlo 10 veces.
			# Pueden ser tanto, a la vez dentro de un solo quantum, o en distintos.

	if pid == 0: # Entran solo los hijos.
		subprocess.run(['ping','-c 2','-i 2','8.8.8.8']) # Lo ejecuta dos veces, esperando dos segundos entre ejecución.
								 # El 'ping' seria el nieto del proceso padre. Se ejecuta 10 veces, 1 por hijo.
		sys.exit()

# Después de que el padre entre 10 veces al 'for', llega aquí.
for i in range(10):
	os.wait() # Espera a que termine 1 hijo como mínimo.

print(time.time()-ahora)
