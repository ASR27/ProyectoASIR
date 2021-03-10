import json, os, requests

creden = []

with open('/vpn/claves/credenciales', 'r') as cred:
	for line in cred:
		clean = line.rstrip()
		creden.append(clean)

usuario = creden[0]
contraseña = creden[1]

#Leemos la clave publica que hemos generado anteriormente en el fichero publica, que usaremos luego en el fichero de configuración

with open('/vpn/claves/publica', 'r') as file:
	pubkey = file.read()


#Consultamos la API y almacenamos los datos en un fichero que usaremos temporalmente
#Si el fichero existe, se borra antes de consultar la API para garantizar que no quedan datos antiguos

if os.path.isfile('/vpn/scripts/perfilesget'):
	os.remove('/vpn/scripts/perfilesget')

r = requests.get('https://albertoasir.duckdns.org/perfiles', auth=(usuario,contraseña))
with open('/vpn/scripts/perfilesget', 'w') as file:
	file.write(r.text)

#Enviamos la clave publica a Django para actualizarla y eliminamos el fichero temporal que hemos creado anteriormente

with open('/vpn/scripts/perfilesget') as json_file:
	data = json.load(json_file)
	for p in data:
		numero = str(p['id'])
		ruta = requests.put('https://albertoasir.duckdns.org/perfiles/' + numero + '/', data={'pubkey':pubkey}, auth=(usuario,contraseña))
		

if os.path.isfile('/vpn/scripts/perfilesget'):
	os.remove('/vpn/scripts/perfilesget')

ruta