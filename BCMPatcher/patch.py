import sys, subprocess, os, struct

#The location of the memory file
MEM_FILE_PATH = "/data/local/tmp/mem"

#The width, in bytes, of a THUMB2 instruction
THUMB2_INST_WIDTH = 4

#The number of copied preamble bytes from the hooked function's header
HOOK_PREAMBLE_BYTES = 6

def write_bytes(addr, bytes):
	'''
	Writes the given sequence of bytes to the given memory address on the device
	'''
	proc = subprocess.Popen(["adb", "shell"], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
	proc.stdin.write("su\n")
	proc.stdin.write("dhdutil -i wlan0 membytes -h 0x%08X %d %s\n" % (addr, len(bytes), bytes.encode("hex")))
	proc.stdin.write("exit\n")
	proc.stdin.write("exit\n")
	proc.wait()

def write_dword(addr, dword):
	'''
	Writes a little-endian DWORD at the given address
	'''
	write_bytes(addr, struct.pack("<I", dword))

def read_bytes(addr, length):
	'''
	Reads the given number of bytes at the given address.
	'''

	#Dumping the bytes into a file
	proc = subprocess.Popen(["adb", "shell"], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
	proc.stdin.write("su\n")
	proc.stdin.write("dhdutil -i wlan0 membytes 0x%08X %d > %s\n" % (addr, length, MEM_FILE_PATH))
	proc.stdin.write("exit\n")
	proc.stdin.write("exit\n")
	proc.wait()

	#Pulling the file
	proc = subprocess.Popen(["adb", "pull", MEM_FILE_PATH], stdout=subprocess.PIPE)
	proc.wait()

	#Parsing and returning the contents
	mem_file = open(os.path.basename(MEM_FILE_PATH), "r")
	output = mem_file.read()
	mem_file.close()
	return output.split(":")[1].strip().replace(" ", "").decode("hex")

def read_dword(addr):
	'''
	Reads a little-endian DWORD at the given address.
	'''
	return struct.unpack("<I", read_bytes(addr, 4))[0]

def encode_thumb2_wide_branch(from_addr, to_addr):
	'''
	Encodes an unconditional THUMB2 wide branch from the given address to the given address.
	'''
	
	if from_addr < to_addr:
		s_bit = 0
		offset = to_addr - from_addr - THUMB2_INST_WIDTH
	else:
		s_bit = 1
		offset = 2**25 - (from_addr + THUMB2_INST_WIDTH - to_addr)

	i1 = (offset >> 24) & 1
	i2 = (offset >> 23) & 1
	j1 = (0 if i1 else 1) ^ s_bit
	j2 = (0 if i2 else 1) ^ s_bit

	b2 = 0b11110000 | (s_bit << 2) | ((offset >> 20) & 0b11)
	b1 = (offset >> 12) & 0xff
	b4 = 0b10010000 | (j1 << 5) | (j2 << 3) | ((offset >> 9) & 0b111)
	b3 = (offset >> 1) & 0xff
	return chr(b1) + chr(b2) + chr(b3) + chr(b4)

def hex_format(s):
    return " ".join(["%02X" % ord(byte) for byte in s])

def main():

	#Reading the arguments
	if len(sys.argv) != 4:
		print "USAGE: %s <FUNCTION_ADDRESS> <HOOK_ADDRESS> <HOOK_FILE>" % sys.argv[0]
		return
	func_addr, hook_addr, hook_file = sys.argv[1:]
	func_addr = int(func_addr, 16)
	hook_addr = int(hook_addr, 16)
        hook_bytes = open(hook_file, 'rb').read()

	#Making sure the functions are DWORD-aligned
	if func_addr % 4 != 0:
		print "Function address must be DWORD-aligned! (%08X)" % func_addr
		return
	if hook_addr % 4 != 0:
		print "Hook address must be DWORD-aligned! (%08X)" % hook_addr
		return

	#Writing the patch to the given memory address
	write_bytes(hook_addr, hook_bytes)

	#Copying the preamble bytes together with appended branch from the function to the hook
	preamble_bytes = read_bytes(func_addr, HOOK_PREAMBLE_BYTES)
        hook_end_addr = hook_addr + len(hook_bytes) + HOOK_PREAMBLE_BYTES
        branch_inst = encode_thumb2_wide_branch(hook_end_addr, func_addr + HOOK_PREAMBLE_BYTES)
        append_bytes = preamble_bytes + branch_inst
        print "[+] Copying preamble and branch to 0x%08X: %s" % (hook_addr + len(hook_bytes), hex_format(append_bytes))
        write_bytes(hook_addr + len(hook_bytes), append_bytes)

	#Lastly, writing the actual branch to the function's preamble
	branch_inst = encode_thumb2_wide_branch(func_addr, hook_addr)
        write_bytes(func_addr, branch_inst)

if __name__ == "__main__":
	main()
