#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests
import Createvm
import startvm
import deletevm
import stopvm
import statusvm

import sys
# from mysql.connector import errorcode


# De kvmController regelt de Database connectie en de administratie van de VM's
class KvmController():
    name = 'Ubuntu_Server'
    filename = '/var/lib/libvirt/save/Ubuntu_Server.img'

    def __init__(self):
        print("KvmController started")



    # Functie die aan de hand van de json request de juiste functie opstart.
    def execute_action(self, data):
        if data['Action'] == 'Create':
            #bla = Createvm.Create
            return 0

        elif data['Action'] == 'Start':
            return startvm.vm_start(data)

        elif data['Action'] == 'Suspend':
            return stopvm.vm_suspend(data)

        elif data['Action'] == 'Remove':
            return deletevm.vm_remove(data)

        elif data['Action'] == 'Status':
            return statusvm.vm_status()
        else:
            return False


# KvmServer ontvangt de request en stuurt het door naar de KvmController
class KvmServer(BaseHTTPRequestHandler):

    # Initialiseert de KvmController
    kvmController = KvmController()

    # Methode die de header opmaakt met code 200 ook wel request accepted
    def _set_headers_record_accepted(self):
        jsonData = statusvm.vm_State.vm_status(self)
        data = {'IP':'192.1.1.1', 'State' : jsonData}
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()


    # Methode die de header opmaakt met code 404 ook wel request not found
    def _set_headers_record_not_found(self):
        self.send_response(200, "test")
        self.send_header("Content-type", "text/html")
        self.end_headers()

        temp = "test"
        self.wfile.write(temp.encode("utf-8"))
        self.wfile.close()


    # Do_get methode word opgeroepen indien de server een get request onvangt
    # Op dit moment word de functie niet gebruikt
    def do_GET(self):
        self._set_headers_record_accepted()

    # do_Post methode word opgeroen indien de server een post request ontvangt
    # De methode decodeert de ontvangen data in  utf-8 en zet het om in json
    # De verwerkte data word aan de KvmController doorgestuurd om vervolgens uitgevoerd te worden
    def do_POST(self):

        # lengte van de ontvangen post request = nodig om de ontvangen data op te slaan
        content_len = int(self.headers['Content-Length'])
        data = self.rfile.read(content_len)
        print(data)
        data = json.loads(data.decode("utf-8"))


        # Indien request correct is stuur code 200 indien incorrect stuur 404
        if (self.kvmController.execute_action(data)):
            self._set_headers_record_accepted()
        else:
            self._set_headers_record_not_found()
        return data


# Run methode definieert de HTTP server en poort
def run(server_class=HTTPServer, handler_class=KvmServer, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()


run()
