import libvirt
import this
import Project_VIRT


class vm_State:

    def vm_status(self):
        data = Project_VIRT.KvmServer.do_POST(self)
        print("Status vm")
        conn = libvirt.open("qemu+tcp://192.168.17.134:16509/system")
        dom = conn.lookupByName(data['_id'])
        status = dom.info()
        print(status)
        return status