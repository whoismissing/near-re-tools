import sys, re

AP_TABLE = { 0b000 : 'All accesses generate a permission fault',
             0b001 : 'Privileged access only',
             0b010 : 'Writes in User mode generate permission faults',
             0b011 : 'Full access',
             0b100 : 'Reserved',
             0b101 : 'Privileged read-only',
             0b110 : 'Privileged/User read-only',
             0b111 : 'Reserved' }

def main():
    if len(sys.argv) != 2:
        print "USAGE: %s <MPU_DUMP>" % sys.argv[0]
        return

    for idx, line in enumerate(open(sys.argv[1],'r').readlines()):
        m = re.match("^([0-9a-f]+) ([0-9a-f]+) ([0-9a-f]+)$", line.strip())
        if not m:
            continue
        base_addr = int(m.group(1), 16)
        size_reg = int(m.group(2), 16)
        access_ctrl = int(m.group(3), 16)

        #Is this region enabled?
        is_enabled = (size_reg & 1) == 1
        if not is_enabled:
            print "Region %d is not enabled" % idx
            continue

        #Print the region's bounds
        region_size = 1 << (((size_reg >> 1) & 0b11111) + 1)
        print "%08X - %08X" % (base_addr, base_addr + region_size)

        #Print the access controls
        ap = (access_ctrl >> 8) & 0b111
        xn = access_ctrl >> 12
        print "AP: %d - %s" % (ap, AP_TABLE[ap])
        print "XN: %d" % xn

if __name__ == "__main__":
    main()
