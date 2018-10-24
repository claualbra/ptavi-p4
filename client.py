#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente UDP que abre un socket a un servidor
"""

import socket
import sys

# Constantes. Dirección IP del servidor y contenido a enviar
SERVER = 'localhost'
PORT = int(sys.argv[2]) #mas de 1024
LINE = ' '.join(sys.argv[3:])
IP = sys.argv[1]

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
# (socket internet,tipo de socket udp) como llamamos a socket
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    print(PORT)
    my_socket.connect((SERVER, PORT))
    print("Enviando:", LINE)
    my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
    data = my_socket.recv(1024)
    print('Recibido -- ', data.decode('utf-8'))

print("Socket terminado.")
