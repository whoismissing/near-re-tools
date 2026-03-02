import sys, struct

#The offset of the RAM on chip
RAM_OFFSET = 0x180000

#The size of the chip's RAM
RAM_SIZE = 0xC0000

#The number of bytes in a DWORD
DWORD_SIZE = 4

#The maximal ring number
BCMPCIE_COMMON_MSGRING_MAX_ID = 4

RING_NAMES = {0 : 'H2D_MSGRING_CONTROL_SUBMIT',
              1 : 'H2D_MSGRING_RXPOST_SUBMIT',
              2 : 'D2H_MSGRING_CONTROL_COMPLETE',
              3 : 'D2H_MSGRING_TX_COMPLETE',
              4 : 'D2H_MSGRING_RX_COMPLETE',
              5 : 'TX_FLOW_RING'}

def read_dword(dump, address):
    '''
    Reads a single DWORD from the RAM dump at the given address
    '''
    address -= RAM_OFFSET
    return struct.unpack("<I", dump[address:address + DWORD_SIZE])[0]

def read_qword(dump, address):
    '''
    Reads a single QWORD form the RAM dump at the given address
    '''
    address -= RAM_OFFSET
    return struct.unpack("<Q", dump[address:address + 2*DWORD_SIZE])[0]

def main():
    if len(sys.argv) != 2:
        print "USAGE: %s <DUMP_FILE>" % sys.argv[0]
        return
    dump_file_path = sys.argv[1]
    dump = open(dump_file_path, 'rb').read()

    #Reading the address of the shared structure (pciedev_shared_t)
    pciedev_shared_t_addr = read_dword(dump, RAM_OFFSET + RAM_SIZE - DWORD_SIZE)
    print "Dumping pciedev_shared_t from 0x%08X" % pciedev_shared_t_addr
    print "-----------------------------------------"
    print "flags:                       0x%08X" %   read_dword(dump, pciedev_shared_t_addr + 0  * DWORD_SIZE)
    print "trap_addr:                   0x%08X" %   read_dword(dump, pciedev_shared_t_addr + 1  * DWORD_SIZE)
    print "assert_exp_addr:             0x%08X" %   read_dword(dump, pciedev_shared_t_addr + 2  * DWORD_SIZE)
    print "assert_file_addr:            0x%08X" %   read_dword(dump, pciedev_shared_t_addr + 3  * DWORD_SIZE)
    print "assert_line:                 0x%08X" %   read_dword(dump, pciedev_shared_t_addr + 4  * DWORD_SIZE)
    print "console_addr:                0x%08X" %   read_dword(dump, pciedev_shared_t_addr + 5  * DWORD_SIZE)
    print "msgtrace_addr:               0x%08X" %   read_dword(dump, pciedev_shared_t_addr + 6  * DWORD_SIZE)
    print "fwid:                        0x%08X" %   read_dword(dump, pciedev_shared_t_addr + 7  * DWORD_SIZE)
    print "total_lfrag_pkt_cnt:         0x%08X" %  (read_dword(dump, pciedev_shared_t_addr + 8  * DWORD_SIZE) & 0xFFFF)
    print "max_host_rxbufs:             0x%08X" % ((read_dword(dump, pciedev_shared_t_addr + 8  * DWORD_SIZE) >> 16) & 0xFFFF)
    print "dma_rxoffset:                0x%08X" %   read_dword(dump, pciedev_shared_t_addr + 9  * DWORD_SIZE)
    print "h2d_mb_data_ptr:             0x%08X" %   read_dword(dump, pciedev_shared_t_addr + 10 * DWORD_SIZE)
    print "d2h_mb_data_ptr:             0x%08X" %   read_dword(dump, pciedev_shared_t_addr + 11 * DWORD_SIZE)
    print "rings_info_ptr:              0x%08X" %   read_dword(dump, pciedev_shared_t_addr + 12 * DWORD_SIZE)
    print "host_dma_scratch_buffer_len: 0x%08X" %   read_dword(dump, pciedev_shared_t_addr + 13 * DWORD_SIZE)
    print "host_dma_scratch_buffer:     0x%08X" %   read_dword(dump, pciedev_shared_t_addr + 14 * DWORD_SIZE)
    print "device_rings_stsblk_len:     0x%08X" %   read_dword(dump, pciedev_shared_t_addr + 15 * DWORD_SIZE)
    print "device_rings_stsblk:         0x%08X" %   read_dword(dump, pciedev_shared_t_addr + 16 * DWORD_SIZE)

    #Dumping the ring buffer physical addresses
    rings_info_ptr = read_dword(dump, pciedev_shared_t_addr + 12 * DWORD_SIZE)
    print 
    print "Dumping ring_info"
    print "-----------------------------------------"
    print "h2d_w_idx_ptr:          0x%08X" % read_dword(dump, rings_info_ptr + 1 * DWORD_SIZE)
    print "h2d_r_idx_ptr:          0x%08X" % read_dword(dump, rings_info_ptr + 2 * DWORD_SIZE)
    print "d2h_w_idx_ptr:          0x%08X" % read_dword(dump, rings_info_ptr + 3 * DWORD_SIZE)
    print "d2h_r_idx_ptr:          0x%08X" % read_dword(dump, rings_info_ptr + 4 * DWORD_SIZE)
    print "h2d_w_idx_hostaddr:     0x%08X" % read_qword(dump, rings_info_ptr + 5 * DWORD_SIZE)
    print "h2d_r_idx_hostaddr:     0x%08X" % read_qword(dump, rings_info_ptr + 7 * DWORD_SIZE)
    print "d2h_w_idx_hostaddr:     0x%08X" % read_qword(dump, rings_info_ptr + 9 * DWORD_SIZE)
    print "d2h_r_idx_hostaddr:     0x%08X" % read_qword(dump, rings_info_ptr + 11 * DWORD_SIZE)

    #Dumping each of the rings' metadata (ring_mem_t)
    ringmem_ptr = read_dword(dump, rings_info_ptr)
    print 
    print "Dumping ring metadata"
    print "-----------------------------------------"
    for i in range(0, BCMPCIE_COMMON_MSGRING_MAX_ID+1):
        idx, ringtype, rsvd = struct.unpack("<HBB", struct.pack("<I", read_dword(dump, ringmem_ptr + i * 4 * DWORD_SIZE)))
        max_items, len_items = struct.unpack("<HH", struct.pack("<I", read_dword(dump, ringmem_ptr + i * 4 * DWORD_SIZE + DWORD_SIZE)))
        ringaddr_ptr = ringmem_ptr + i * 4 * DWORD_SIZE + 2*DWORD_SIZE
        ringaddr = read_qword(dump, ringaddr_ptr)
        print "ring:      %d"                   % i
        print "idx:       %d"                   % idx
        print "ring name: %s"                   % RING_NAMES[i]
        print "ringtype:  %d"                   % ringtype
        print "rsvd:      %d"                   % rsvd
        print "max_items: %d"                   % max_items
        print "len_items: %d"                   % len_items
        print "ringaddr:  0x%08X (mem 0x%08X)"  % (ringaddr, ringaddr_ptr)
        print "ring size: %d"                   % (max_items * len_items)
        print 

if __name__ == "__main__":
    main()
