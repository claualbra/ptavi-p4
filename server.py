#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Clase (y programa principal) para un servidor de eco en UDP simple."""

import socketserver
import sys
import time
import json


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """Inicializo el diccionario de usuarios."""

    dicc = {}

    def json2register(self):
        """Descargo fichero json en el diccionario."""
        try:
            with open('registered.json', 'r') as jsonfile:
                self.dicc = json.load(jsonfile)
        except:
            pass

    def register2json(self):
        """
        Escribir diccionario.

        En formato json en elfichero registered.json.
        """
        with open('registered.json', 'w') as jsonfile:
            json.dump(self.dicc, jsonfile, indent=4)

    def handle(self):
        """
        Recibo el mensaje del cliente.

        En el caso de que la peticion sea un
        register guardo la informacion en un diccionario.
        """
        self.json2register()
        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
        linea = ''
        for line in self.rfile:
            linea += line.decode('utf-8')
        if linea != '\r\n':
            print("El cliente nos manda ", linea)
            (peticion, address, sip, expires) = linea.split()
            if peticion == 'REGISTER':
                IP = self.client_address[0]
                user = address.split(':')[1]
                # Timpo actual mas expiracion
                Time = time.time() + int(expires)
                TimeExp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(Time))
                now = time.strftime('%Y-%m-%d %H:%M:%S',
                                    time.gmtime(time.time()))
                self.dicc[user] = {'address': IP, 'expires': TimeExp}
                user_del = []
                for user in self.dicc:
                    if now >= self.dicc[user]['expires']:
                        user_del.append(user)
                for user in user_del:
                    del self.dicc[user]
                self.register2json()
                print(self.dicc)


if __name__ == "__main__":
    # Listens at localhost ('') port 6001
    # and calls the EchoHandler class to manage the request
    serv = socketserver.UDPServer(('', int(sys.argv[1])), SIPRegisterHandler)

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
