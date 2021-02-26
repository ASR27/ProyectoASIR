import json, os

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

#Leemos la clave publica que hemos generado anteriormente en el fichero publickey

with open('/home/asr/publickey', 'r') as file:
	pubkey = file.read()

#Consultamos la API y almacenamos los datos en un fichero que usaremos temporalmente
#Si el fichero existe, se borra antes de consultar la API para garantizar que no quedan datos antiguos

if os.path.isfile('/home/asr/perfilesget'):
	os.remove('/home/asr/perfilesget')
os.system("http -a " + usuario + ":" + contraseña + " GET 10.0.20.1:8000/perfiles/ >> /home/asr/perfilesget")

#Leemos del fichero temporal el id de nuestro usuario y enviamos una peticion a la API para actualizar
	#la clave publica del cliente por la actual

with open('/home/asr/perfilesget') as json_file:
	data = json.load(json_file)
	for p in data:
		numero = str(p['id'])
		ruta = "http -a " + usuario + ":" + contraseña + " PUT 10.0.20.1:8000/perfiles/" + numero + "/" + " " + "pubkey='" + pubkey + "'"

os.system(ruta)

#Una vez actualizada la clave publica del usuario, borramos el fichero temporal
		
if os.path.isfile('/home/asr/perfilesget'):
	os.remove('/home/asr/perfilesget')
