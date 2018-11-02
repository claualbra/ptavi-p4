#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import time
import json


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    dicc = {}

    def json2register(self):
        try:
            with open('registered.json', 'r') as jsonfile:
                self.dicc = json.load(jsonfile)
        except FileNotFoundError:
            pass

    def register2json(self):
        """
        Escribir diccionario en formato json en el fichero registered.json
        """
        with open('registered.json', 'w') as jsonfile:
            json.dump(self.dicc, jsonfile, indent=4)


    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
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
                Time = time.time() + int(expires)
                TimeExp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(Time))
                if int(expires) != 0:
                    self.dicc[user] = {'address': IP,'expires': TimeExp}
                elif int(expires) == 0:
                    try:
                        del self.dicc[user]
                    except KeyError:
                        pass
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
