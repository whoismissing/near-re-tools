import struct
from profiles import *

DWORD_SIZE = 4

def read_dword(dump, address):
	'''
	Reads a single DWORD at the given address from the RAM dump
	'''
	try:
		address -= get_profile_def("ram_dump_offset")
		return struct.unpack("<I", dump[address:address + DWORD_SIZE])[0]
	except Exception, e:
		print "Falied to read memory at 0x%08X" % (address + get_profile_def("ram_dump_offset"))
		raise e

