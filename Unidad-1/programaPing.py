import subprocess, time

# Le asignamos a una variable el tiempo exacto actuañ
ahora = time.time()

# Accion -> ping
# Contador de veces -> -c 1
# Direccion -> 8.8.8.8
for i in range(10):
	subprocess.run(['ping','-c 1','8.8.8.8'])

# Calculamos cuanto tiempo hay desde el ping al print
print(time.time()-ahora)
