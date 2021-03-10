import json, os, os.path, requests

creden = []

with open('/home/webuser/credencialesserver', 'r') as cred:
	for line in cred:
		clean = line.rstrip()
		creden.append(clean)

usuario = creden[0]
contraseña = creden[1]

#Consultamos la API y almacenamos los datos en un fichero que usaremos temporalmente
#Si el fichero existe, se borra antes de consultar la API para garantizar que no quedan datos antiguos

if os.path.isfile('/home/webuser/aulasauto'):
	os.remove('/home/webuser/aulasauto')

r = requests.get('https://albertoasir.duckdns.org/aulas', auth=(usuario,contraseña))
with open('/home/webuser/aulasauto', 'w') as file:
	file.write(r.text)

#Leemos del fichero temporal los datos con los que generaremos nuestros ficheros de configuración de wireguard

#Con esto creamos en el servidor un fichero de configuración por cada taller disponible
#en el que incluimos a todos los alumnos conectados

with open('/home/webuser/aulasauto') as json_file:
	data = json.load(json_file)
	for p in data:
		f = open('/home/webuser/' + str(p['nombre']) + 'server.conf', 'w')
		f.close()
		g = open('/home/webuser/' + str(p['nombre']) + 'server.conf', 'w')
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
		#Actualizamos la interfaz en caliente sin cortar la conexión
		os.system('sudo wg-quick strip /etc/wireguard/' + str(p['nombre']) + 'server.conf > /home/webuser/' + str(p['nombre']) + 'server.conf.strip')
		os.system('sudo wg syncconf < /home/webuser/' + str(p['nombre']) + 'server.conf.strip')

#Una vez creados los ficheros de configuración, eliminamos el fichero temporal

if os.path.isfile('/home/webuser/aulasauto'):
	os.remove('/home/webuser/aulasauto')