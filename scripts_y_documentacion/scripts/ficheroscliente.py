import json, os, os.path

###########################################################################################
#Todas las rutas de ficheros son temporales
###########################################################################################

#Leemos el usuario y contraseña del fichero de credenciales
#Este fichero no estará incluido en la ISO, se creara más tarde

creden = []

with open('/home/asr/credenciales', 'r') as cred:
	for line in cred:
		clean = line.rstrip()
		creden.append(clean)

usuario = creden[0]
contraseña = creden[1]

#Leemos la clave privada que hemos generado anteriormente en el fichero privatekey, que usaremos luego en el fichero de configuración

with open('/home/asr/privatekey', 'r') as file:
	privkey = file.read()

#Consultamos la API y almacenamos los datos en un fichero que usaremos temporalmente
#Si el fichero existe, se borra antes de consultar la API para garantizar que no quedan datos antiguos

if os.path.isfile('/home/asr/conexionesauto'):
	os.remove('/home/asr/conexionesauto')
os.system("http -a " + usuario + ":" + contraseña + " GET 10.0.20.1:8000/conexiones/ >> /home/asr/conexionesauto")

#Leemos del fichero temporal los datos con los que generaremos nuestros ficheros de configuración de wireguard
#Esto creara en el cliente un fichero por cada taller al que se le permita la conexión

with open('/home/asr/conexionesauto') as json_file:
	data = json.load(json_file)
	for p in data:
		f = open('/home/asr/' + str(p['interfaz']['nombre']) + '.conf', 'w')
		f.close()
		g = open('/home/asr/' + str(p['interfaz']['nombre']) + '.conf', 'a')
		g.write('[Interface]\n')
		g.write('Address = ' + str(p['ip']) + '\n')
		g.write('PrivateKey = ' + privkey + '\n')
		g.write('\n')
		g.write('[Peer]\n')
		g.write('PublicKey = ' + str(p['interfaz']['serverpubkey']) + '\n')
		g.write('Endpoint = ' + str(p['interfaz']['endpoint']) + '\n')
		g.close()

#Una vez creados los ficheros de configuración, eliminamos el fichero temporal

if os.path.isfile('/home/asr/conexionesauto'):
	os.remove('/home/asr/conexionesauto')