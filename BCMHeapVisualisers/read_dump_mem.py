import sys, struct
from utils import *
from profiles import *

def main():

	#Reading the agruments
	if len(sys.argv) < 5:
		print "USAGE: %s <PROFILE_NAME> <DUMP_FILE> <0xADDRESS> <NUM_DWORDS>" % sys.argv[0]
		return

        profile_name = sys.argv[1]
	dump_file = sys.argv[2]
	addr = int(sys.argv[3], 16)
        num_dwords = int(sys.argv[4])
        set_profile(profile_name)

        dump = open(dump_file, 'rb').read()
        for i in range(0, num_dwords):
            print "0x%08X : 0x%08X" % (addr + i * DWORD_SIZE, read_dword(dump, addr + i * DWORD_SIZE))

if __name__ == "__main__":
	main()
