import json, os, os.path

###########################################################################################
#Todas las rutas de ficheros son temporales
###########################################################################################

#Leemos el usuario y contraseña del fichero de credenciales

creden = []

with open('/home/asr/credenciales', 'r') as cred:
	for line in cred:
		clean = line.rstrip()
		creden.append(clean)

usuario = creden[0]
contraseña = creden[1]

#Consultamos la API y almacenamos los datos en un fichero que usaremos temporalmente
#Si el fichero existe, se borra antes de consultar la API para garantizar que no quedan datos antiguos

if os.path.isfile('/home/asr/aulasauto'):
	os.remove('/home/asr/aulasauto')
os.system("http -a " + usuario + ":" + contraseña + " GET 10.0.20.1:8000/aulas/ >> /home/asr/aulasauto")

#Leemos del fichero temporal los datos con los que generaremos nuestros ficheros de configuración de wireguard
#Con esto creamos en el servidor un fichero de configuración por cada taller disponible
	#en el que incluimos a todos los alumnos conectados

with open('/home/asr/aulasauto') as json_file:
	data = json.load(json_file)
	for p in data:
		f = open('/home/asr/' + str(p['nombre']) + 'server.conf', 'w')
		f.close()
		g = open('/home/asr/' + str(p['nombre']) + 'server.conf', 'w')
		g.write('[Interface]\n')
		g.write('Address =' + str(p['serverip']) + '\n')
		g.write('PrivateKey = ' + str(p['serverprivkey']) + '\n')
		g.write('ListenPort = ' + str(p['port']) + '\n')
		g.write('\n')
		for r in p['clientes']:
			g.write('[Peer]\n')
			g.write('PublicKey = ' + str(r['pubkey']) + '\n')
			g.write('AllowedIPs = ' + str(p['subred']) + '/24' + '\n')
			g.write('\n')
		g.close()

#Una vez creados los ficheros de configuración, eliminamos el fichero temporal

if os.path.isfile('/home/asr/aulasauto'):
	os.remove('/home/asr/aulasauto')
