#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import Createvm
import startvm
import deletevm
import stopvm
import statusvm
import sys
# temp = statusvm.vm_State(str())
# De kvmController regelt de Database connectie en de administratie van de VM's


class KvmController():
    name = 'Ubuntu_Server'
    filename = '/var/lib/libvirt/save/Ubuntu_Server.img'

    #Database, werkt nog niet
    def __init__(self):
        print("KvmController started")

    # Functie die aan de hand van de json request de juiste functie opstart.
    def execute_action(self, data):

        if data['Action'] == 'Create':
            temp = Createvm.Create()
            return temp.vm_create(data)

        elif data['Action'] == 'Start':
            temp = startvm.Start()
            return temp.vm_start(data)

        elif data['Action'] == 'Suspend':
            temp = stopvm.Stop()
            return temp.vm_suspend(data)

        elif data['Action'] == 'Remove':
            temp = deletevm.Del()
            return temp.vm_remove(data)

        elif data['Action'] == 'Status':
            temp = statusvm.vm_State()
            return temp.vm_status(data)
        else:
            return False



# KvmServer ontvangt de request en stuurt het door naar de KvmController
class KvmServer(BaseHTTPRequestHandler, ):

    # Initialiseert de KvmController
    kvmController = KvmController()

    # Methode die de header opmaakt met code 200 ook wel request accepted
    def _set_headers_record_accepted(self, data):
        temp = statusvm.vm_State()
        bla = temp.vm_status(data)
        IP = '10.0.0.10'
        data2 = {'IP': IP, 'State' : str(bla)}
        data3 = json.dumps(data2, indent=4, sort_keys=True)
        # data1 = json.loads(data3)
        print(data3)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(data3.encode("utf-8"))



    # Methode die de header opmaakt in het geval van ID not found, hierdoor een response van 404, ook wel value not
    # found
    def _set_headers_record_not_found(self):
        self.send_response(404)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        temp = "test"
        self.wfile.write(temp.encode("utf-8"))
        self.wfile.close()

    # Methode die de header opmaakt in het geval van een IP not found, hierdoor een response  van 401, ook wel not
    # authorised
    def _set_headers_ip_not_found(self):
        self.send_response(401)
        self.send_header('Content-type', 'application/json')
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
        try:
            content_len = int(self.headers['Content-Length'])
            data = self.rfile.read(content_len)
            data = json.loads(data.decode("utf-8"))
            ip = str(self.client_address[0])
            ipstr = ' '.join(IpAdressen)
            print("Connectie vanaf: " + ip)
            print("Is deze deel van: " + ipstr + " ?")
            if ip in IpAdressen:
                print("Ja, proceed.")
                if (self.kvmController.execute_action(data)):
                    self._set_headers_record_accepted(data)
                else:
                    self._set_headers_record_not_found()
            else:
                print("Nee, abort.")
                self._set_headers_ip_not_found()

        except Exception as err:
            print(err, file=sys.stderr)


class HTTPD():
    # Run methode definieert de HTTP server en poort
    def run(server_class=HTTPServer, handler_class=KvmServer):
        try:
            port = int(input("We gaan nu starten welke poort wil je gebruiken?\n"))
        except ValueError:
            port = 8000
            print('Joe!')


        antw = str(input("Is port: " + str(port) + " de juiste?(y/n)\n"))
        if antw =='':
            print('Joe!')
        if antw not in ['y', '']:
            while antw is not "y":
                port = input("Welke poort wil je gebruiken?\n")
                antw = str(input("Is port: " + str(port) + "de juiste?(y/n)\n"))
        global IpAdressen
        IpAdressen = ["127.0.0.1"]
        while True
            NieuwIP = input("Wilt u een nieuw IP adres toevoegen voor de connectie?(y/n) ")
            if NieuwIP == 'n' or '':
                break
            toevoeg = input("Welk IP adres wilt u toevoegen?: \n")
            IpAdressen.append(toevoeg)


        # check of ip goed gaat
        print(IpAdressen)
        print('Dank u, een moment.')
        server_address = ('', port)
        httpd = server_class(server_address, handler_class)
        print("Gestart, klaar voor Commando's.")
        httpd.serve_forever()

HTTPD.run()


