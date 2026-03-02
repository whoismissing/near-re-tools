import sys, struct
from utils import *
from profiles import *

#The height of each rendered block
RENDER_HEIGHT = 30

#The height of the space between rows
SPACER_HEIGHT = 10

#The horizontal scale factor
SCALE_FACTOR = 0.5

def generate_chunk_div(curr, size, min_offset, top):
	style = "style=\"position: absolute; left: %f; top: %d; width: %f; height: %d; background: red;\"" % ((curr - min_offset) * SCALE_FACTOR, top, size * SCALE_FACTOR, RENDER_HEIGHT)
	title = "title=\"0x%08X , size: 0x%X\"" % (curr, size)
	return "<div %s %s></div>" % (style, title)

def main():

	#Reading the agruments
	if len(sys.argv) < 4:
		print "USAGE: %s <PROFILE_NAME> <DUMP_FILE> [<DUMP_FILES> ...] <OUTPUT_FILE>" % sys.argv[0]
		return
        profile_name = sys.argv[1]
	dump_file_paths = sys.argv[2:-1]
	output_file_path = sys.argv[-1]
        set_profile(profile_name)

	#Reading each of the heaps in the dumped files
	heaps = []
	for dump_file_path in dump_file_paths:
		#Going over each chunk in the freelist
		dump = open(dump_file_path, "rb").read()
		curr = read_dword(dump, get_profile_def("freelist_address"))
		nodes = []
		while curr != 0:
			size = read_dword(dump, curr)
			next = read_dword(dump, curr + DWORD_SIZE)
			nodes.append((curr, size))
			curr = next
		heaps.append(nodes)

	#Finding the bounds
	min_offset = min([min([curr for (curr, size) in heap]) for heap in heaps])
	scale_factor = 0.5

	#Rendering the heaps to an HTML file
	output_file = open(output_file_path, "w")
	output_file.write("<html>\n")
	output_file.write("  <body>\n")
	output_file.write("    <div id=\"container\">");

	for idx, heap in enumerate(heaps):
		output_file.write("\n")
		top = (RENDER_HEIGHT +SPACER_HEIGHT)*idx + RENDER_HEIGHT	
		output_file.write("\n".join(["        " +  generate_chunk_div(curr, size, min_offset, top) for (curr,size) in heap]))

	output_file.write("\n")	
	output_file.write("    </div>\n")
	output_file.write("  </body>\n")
	output_file.write("</html>\n")
	output_file.close()

if __name__ == "__main__":
	main()
