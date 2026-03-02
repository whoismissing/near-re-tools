import sys, struct
from profiles import *
from utils import *

def main():

	#Reading the agruments
	if len(sys.argv) != 4:
		print "USAGE: %s <PROFILE_NAME> <DUMP_FILE> <OUTPUT_FILE>" % sys.argv[0]
		return
	profile_name, dump_file_path, output_file_path = sys.argv[1:]
        set_profile(profile_name)

	#Going over each chunk in the freelist
	dump = open(dump_file_path, "rb").read()
	curr = read_dword(dump, get_profile_def("freelist_address"))
	nodes = []
	while curr != 0:
                try:
		    size = read_dword(dump, curr)
		    next = read_dword(dump, curr + DWORD_SIZE)
                except:
                    print "Failed to read next chunk pointer! curr: %08x" % curr
                    break
		nodes.append((curr, size))
		curr = next

	#Rendering the graph to a DOT file
	output_file = open(output_file_path, "w")
	output_file.write("digraph g{\n")
	output_file.write("    rankdir=LR;\n")
	output_file.write("    %s;\n" % "->".join(["\"address: 0x%08X | size: 0x%08X\"" % (curr, size) for (curr,size) in nodes]))
	output_file.write("}")

if __name__ == "__main__":
	main()
