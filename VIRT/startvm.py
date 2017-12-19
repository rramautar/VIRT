import libvirt
import sys
import this

def vm_start(data):
    print("Starting Vm")
    dom = ''
    id = 0

    print("Starting Vm")
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