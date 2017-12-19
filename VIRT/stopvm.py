import libvirt
import sys
import this


def vm_suspend(data):
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