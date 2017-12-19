#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import libvirt
# import mysql.connector
import sys
# from mysql.connector import errorcode


# De kvmController regelt de Database connectie en de administratie van de VM's
class KvmController():
    name = 'Ubuntu_Server'
    filename = '/var/lib/libvirt/save/Ubuntu_Server.img'
    dbConn = None

    # def init_db_connection(self):
    #     try:
    #         dbConn = mysql.connector.connect(user='Team5', password='Team5!', host='86.92.147.175', database='VIRT')
    #     except mysql.connector.Error as err:
    #         if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    #             print("Something is wrong with your user name or password")
    #         elif err.errno == errorcode.ER_BAD_DB_ERROR:
    #             print("Database does not exist")
    #         else:
    #             print(err)
    #     print("DB Connection started")

    # init methode word aangeroepen als de klass aangemaakt word. Hierin word de database connectie gemaakt.
    def __init__(self):
        print("KvmController started")
        # self.init_db_connection()

    # Create Vm
    def vm_create(self, data):
        print("Creating Vm")

        ram = 512
        cpu = 1
        stor = 0
        conn = libvirt.open("qemu+tcp://192.168.17.134:16509/system")
        def xmlconfig(name, ram, stor, cpu):
            name = str(name)
            ram = str(ram)
            stor = str(stor)
            cpu = str(cpu)

            XML = """<domain type='kvm'>
                 <name>Ubuntu_Server</name>
                 <memory unit='M'>"""+ ram + """"</memory>
                 <currentMemory>512</currentMemory>
                 <vcpu>1</vcpu>
                 <os>
                   <type>hvm</type>
                   <boot dev='hd'/>
                 </os>
                 <features>
                   <acpi/>
                 </features>
                 <clock offset='utc'/>
                 <on_poweroff>destroy</on_poweroff>
                 <on_reboot>restart</on_reboot>
                 <on_crash>restart</on_crash>
                 <devices>
                   <emulator>/usr/bin/kvm</emulator>
                   <disk type='block' device='disk'>
                     <source dev='/dev/mapper/Ubuntu_Server.img'/>
                     <target dev='hda' bus='ide'/>
                   </disk>
                   <disk device="cdrom" type="file">
                           <source file="/var/lib/libvirt/images/ubuntu-16.04.3-server-amd64.iso"/>
                           <driver name="qemu" type="raw" />
                           <target bus="ide" dev="hdc" />
                           <readyonly />
                           <address bus="1" controller="0" target="0" type="drive" unit="0" />
                       </disk>
                   <interface type='bridge'>
                     <source bridge='virbr0'/>
                   </interface>
                   <input type='tablet' bus='usb'/>
                   <input type='mouse' bus='ps2'/>
                   <graphics type='vnc' port='-1' listen='127.0.0.1'/>
                 </devices>
               </domain>"""
            return XML

        dom = conn.createXML(xmlconfig(self.name, ram, stor, cpu), 0)
        if dom == None:
            print('Failed to create a domain from an XML definition.', file=sys.stderr)
            return False

        print('Guest ' + dom.name() + ' has booted', file=sys.stderr)
        return True

    # Start Vm
    def vm_start(self, data):
        print("Starting Vm")
        dom = ''
        id = 0

        conn = libvirt.open("qemu+tcp://192.168.17.134:16509/system")

        if conn == None:
            print('Failed to open connection to qemu+tcp://192.168.17.134:16509/system', file=sys.stderr)
            return False

        try:
            dom = conn.lookupByName(this.name)
            print(str(dom))
            if dom != '':
                print('Domain is allready running')
        except:
            print('No vm found with name: ' + this.name + '. Starting a new vm.')

        if dom == '':
            id = conn.restore(this.filename)
            if id != 0:
                print('Unable to restore guest from ' + this.filename, file=sys.stderr)

            dom = conn.lookupByName(this.name)
            if dom == None:
                print('Cannot find guest that was restored', file=sys.stderr)

            print('Guest state restored from ' + this.filename, file=sys.stderr)

        return True

    # Suspend Vm
    def vm_suspend(self, data):
        print("Suspending Vm")
        conn = libvirt.open("qemu+tcp://192.168.17.134:16509/system")
        if conn == None:
            print('Failed to open connection to qemu+tcp://192.168.17.134:16509/system', file=sys.stderr)

        dom = conn.lookupByName(name)

        if dom == None:
            print('Cannot find guest to be saved.', file=sys.stderr)
            return False

        if info == None:
            print('Cannot check guest state', file=sys.stderr)
            return False

        state, reason = dom.state()
        if state != libvirt.VIR_DOMAIN_RUNNING:
            print('Not saving guest that is not running', file=sys.stderr)
            return False

        if dom.save(this.filename) < 0:
            print('Unable to save guest to ' + this.filename, file=sys.stderr)
            return False

        print('Guest state saved to ' + this.filename, file=sys.stderr)
        dom.shutdown()
        conn.close()
        exit(0)
        return True

    #  Stop Vm
    def vm_stop(self, data):
        print("Stop Vm")
        return True

    # Remove Vm
    def vm_remove(self, data):
        print("Remove vm")
        conn = libvirt.open("qemu+tcp://192.168.17.134:16509/system")
        if conn == None:
            print('Failed to open connection to qemu+tcp://192.168.17.134:16509/system', file=sys.stderr)

        dom = conn.lookupByName(this.name)
        if dom == '':
            print('Could not find domain.')

        dom.destroy()
        print('Domain ' + this.name + ' was Destroyed')
        return True

    # Status Vm
    def vm_status(self, data):
        print("Status vm")
        conn = libvirt.open("qemu+tcp://192.168.17.134:16509/system")
        dom = conn.lookupByName(name)
        status = dom.info()
        print(status)
        return True

    # Functie die aan de hand van de json request de juiste functie opstart.
    def execute_action(self, data):
        if data['Action'] == 'Create':
            return self.vm_create(data)
        elif data['Action'] == 'Start':
            return self.vm_start(data)
        elif data['Action'] == 'Suspend':
            return self.vm_suspend(data)
        elif data['Action'] == 'Stop':
            return self.vm_stop(data)
        elif data['Action'] == 'Remove':
            return self.vm_remove(data)
        elif data['Action'] == 'Status':
            return self.vm_status(data)
        else:
            return False


# KvmServer ontvangt de request en stuurt het door naar de KvmController
class KvmServer(BaseHTTPRequestHandler):
    # Initialiseert de KvmController
    kvmController = KvmController()

    # Methode die de header opmaakt met code 200 ook wel request accepted
    def _set_headers_record_accepted(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    # Methode die de header opmaakt met code 404 ook wel request not found
    def _set_headers_record_not_found(self):
        self.send_response(404)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

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

        data = json.loads(data.decode("utf-8"))

        # Indien request correct is stuur code 200 indien incorrect stuur 404
        if (self.kvmController.execute_action(data)):
            self._set_headers_record_accepted()
        else:
            self._set_headers_record_not_found()


# Run methode definieert de HTTP server en poort
def run(server_class=HTTPServer, handler_class=KvmServer, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()


run()
