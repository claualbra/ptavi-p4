#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    dicc = {}

    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        pet = self.rfile.read()
        print(str(self.client_address))
        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
        for line in pet:
            print(pet)
            linea = line.decode('utf-8')
            if linea != '\r\n':
                print("El cliente nos manda ", linea)
                (peticion, address, sip, expires) = linea.split()
                if peticion == 'REGISTER':
                    IP = self.client_address[0]
                    user = address.split(':')[1]
                    self.dicc[user] = {'address': IP,'expires': expires}
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
