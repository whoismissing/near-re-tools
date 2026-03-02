import sys, struct

#The offset of the RAM dump file
RAM_DUMP_OFFSET = 0x180000

#The address of the pointer to the first timer
#TIMERS_ADDRESS = 0x180E6C #Address of the Nexus 5 (bcm4339_6.37.34.40)
TIMERS_ADDRESS = 0x180708 #Address on the Nexus 6P (bcm4358_7.112.201.1)

#The number of bytes in a DWORD
DWORD_SIZE = 4

def read_dword(dump, address):
    '''
    Reads a single DWORD from the RAM dump at the given address
    '''
    address -= RAM_DUMP_OFFSET
    return struct.unpack("<I", dump[address:address + DWORD_SIZE])[0]


def main():
    if len(sys.argv) != 2:
        print "USAGE: %s <DUMP_FILE>" % sys.argv[0]
        return
    dump_file_path = sys.argv[1]
    dump = open(dump_file_path, 'rb').read()

    #Iterating over all the timers and dumping them
    timer = TIMERS_ADDRESS
    while timer != 0:
        next_timer   = read_dword(dump, timer)
        timeout      = read_dword(dump, timer+DWORD_SIZE)
        function_ptr = read_dword(dump, timer+DWORD_SIZE*2)
        argument     = read_dword(dump, timer+DWORD_SIZE*3)
        expired      = read_dword(dump, timer+DWORD_SIZE*4)

        print "Timer   : 0x%08X"          % timer
        print "Timeout : %d milliseconds" % timeout
        print "Function: 0x%08x"          % function_ptr
        print "Argument: 0x%08x"          % argument
        print "Expired : %r"              % (expired != 0)
        print "------------------------------"
        timer = next_timer

if __name__ == "__main__":
    main()
