import json, os, os.path, requests

creden = []

with open('/vpn/claves/credenciales', 'r') as cred:
	for line in cred:
		clean = line.rstrip()
		creden.append(clean)

usuario = creden[0]
contraseña = creden[1]

#Consultamos la API y almacenamos los datos en un fichero que usaremos temporalmente
#Si el fichero existe, se borra antes de consultar la API para garantizar que no quedan datos antiguos

if os.path.isfile('/vpn/scripts/conexionesauto'):
	os.remove('/vpn/scripts/conexionesauto')

r = requests.get('https://albertoasir.duckdns.org/conexiones', auth=(usuario,contraseña))
with open('/vpn/scripts/conexionesauto', 'w') as file:
	file.write(r.text)

#Leemos la clave privada que hemos generado anteriormente en el fichero privada, que usaremos luego en el fichero de configuración

with open('/vpn/claves/privada', 'r') as file:
	privkey = file.read()


with open('/vpn/scripts/conexionesauto') as json_file:
	data = json.load(json_file)
	for p in data:
		f = open('/vpn/scripts/' + str(p['interfaz']['nombre']) + '.conf', 'w')
		f.close()
		g = open('/vpn/scripts/' + str(p['interfaz']['nombre']) + '.conf', 'a')
		g.write('[Interface]\n')
		g.write('Address = ' + str(p['ip']) + '\n')
		g.write('PrivateKey = ' + privkey + '\n')
		g.write('\n')
		g.write('[Peer]\n')
		g.write('PublicKey = ' + str(p['interfaz']['serverpubkey']) + '\n')
		g.write('Endpoint = ' + str(p['interfaz']['endpoint']) + '\n')
		g.close()
		#Actualizamos la interfaz en caliente sin cortar la conexión
		os.system('sudo wg-quick strip ' + str(p['nombre']) + 'server.conf > /vpn/scripts/' + str(p['nombre']) + 'server.conf.strip')
		os.system('sudo wg syncconf < /vpn/scripts/' + str(p['nombre']) + 'server.conf.strip')

#Una vez creados los ficheros de configuración, eliminamos el fichero temporal

if os.path.isfile('/vpn/scripts/conexionesauto'):
 	os.remove('/vpn/scripts/conexionesauto')