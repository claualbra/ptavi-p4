#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente UDP que abre un socket a un servidor
"""

import socket
import sys

# Constantes. Dirección IP del servidor y contenido a enviar
SERVER = sys.argv[1]
PORT = int(sys.argv[2])
PETICION = sys.argv[3]
ADRESSS = sys.argv[4]
EXPIRES = sys.argv[5]

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((SERVER, PORT))
    print("Enviando:", PETICION.upper() + ' sip:'+ ADRESSS + ' SIP/2.0')
    print("Expires: " + EXPIRES)
    my_socket.send(bytes(PETICION.upper() + ' sip:'+ ADRESSS + ' SIP/2.0',
                        'utf-8') + b'\r\n' + bytes(EXPIRES, 'utf-8') + b'\r\n')
    data = my_socket.recv(1024)
    print('Recibido -- ', data.decode('utf-8'))

print("Socket terminado.")
