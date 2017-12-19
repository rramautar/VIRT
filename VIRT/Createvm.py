import libvirt
import uuid
import sys
import Project_VIRT






class Create:
    data = Project_VIRT.do_POST()
    id = data['_id']
    os = "Ubuntu"
    ip = "172.0.0.1"
    # Create Vm
    def vm_create(self):
        print("Creating Vm")
        data = Project_VIRT.do_POST()
        ram = 512
        name = data['_id']
        cpu = 1
        stor = 0

        conn = libvirt.open("qemu+tcp://192.168.17.134:16509/system")

        def xmlconfig(ram, stor, cpu, uid):
            ram = str(ram)
            stor = str(stor)
            cpu = str(cpu)
            uid = str(uid)

            XML = """<domain type='kvm'>
                     <name>""" + uid + """</name>
                     <memory unit='M'>""" + ram + """</memory>
                     <currentMemory>""" + ram + """</currentMemory>
                     <vcpu>""" + cpu + """</vcpu>
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
                               <source file="/var/lib/libvirt/images/ubuntu-16.04.3-desktop-amd64.iso"/>
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


        dom = conn.createXML(xmlconfig(ram, stor, cpu, id), 0)
        if dom == None:
            print('Failed to create a domain from an XML definition.', file=sys.stderr)
            return False



        print('Guest ' + dom.name() + ' has booted', file=sys.stderr)

        return True

    vm_create(data)
