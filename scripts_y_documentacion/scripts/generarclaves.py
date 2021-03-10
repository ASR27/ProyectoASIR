import json, os, requests

if not os.path.isfile('/vpn/claves/privada'):
	os.system('wg genkey > /vpn/claves/privada')

if not os.path.isfile('/vpn/claves/publica'):
	os.system('(wg pubkey < /vpn/claves/privada) > /vpn/claves/publica')