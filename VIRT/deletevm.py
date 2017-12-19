import libvirt
import sys
import this


def vm_remove(data):
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