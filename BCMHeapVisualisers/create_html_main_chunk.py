import sys, struct
from utils import *
from profiles import *

#The height of each rendered block
RENDER_HEIGHT = 30

#The height of the space between rows
SPACER_HEIGHT = 10

#The horizontal scale factor
SCALE_FACTOR = 0.5

#The size of a chunk's header
CHUNK_HEADER_SIZE = 2*DWORD_SIZE

#Marker values to indicate a chunk's type
FREE_CHUNK = 0
INUSE_CHUNK = 1

def generate_chunk_div(curr, size, min_offset, top, type):
	color = "gray" if type == FREE_CHUNK else "red"
	style = ("".join(["style=\"position: absolute; ",
			  "border: 1px solid black; ",
			  "opacity: 0.75;",
			  "left: %f;",
			  "top: %d;",
			  "width: %f;",
			  "height: %d;",
			  "background: %s;\""])) % ((curr - min_offset) * SCALE_FACTOR, top, size * SCALE_FACTOR, RENDER_HEIGHT, color)
        title = "title=\"0x%08X , size: 0x%X, end: 0x%X\"" % (curr, size, curr+size+8)
	return "<div %s %s></div>" % (style, title)

def main():

	#Reading the agruments
	if len(sys.argv) < 4:
		print "USAGE: %s <PROFILE_NAME> <DUMP_FILE> [<DUMP_FILES> ...] <OUTPUT_FILE> [-noinuse]" % sys.argv[0]
		return

	noinuse = False
	if sys.argv[-1] == "-noinuse":
		noinuse = True
		sys.argv = sys.argv[:-1]

        profile_name = sys.argv[1]
	dump_file_paths = sys.argv[2:-1]
	output_file_path = sys.argv[-1]
        set_profile(profile_name)

	#Reading each of the heaps in the dumped files
	heaps = []
	for dump_file_path in dump_file_paths:
		
		#Going over each chunk in the free-list starting at the main chunk
		dump = open(dump_file_path, "rb").read()
		curr = get_profile_def("main_chunk_address")
		nodes = []
		while curr != 0:
			size = read_dword(dump, curr)
			next = read_dword(dump, curr + DWORD_SIZE)
			nodes.append((curr, size, FREE_CHUNK))

			if not noinuse: 
				#If the next free chunk isn't immediately after this one, there are in-use
				#chunks between them. Find and add all of them.
				cinuse = curr + CHUNK_HEADER_SIZE + size
				while cinuse != next and cinuse < get_profile_def("max_heap_address"):
					inuse_size = read_dword(dump, cinuse)
					nodes.append((cinuse, inuse_size, INUSE_CHUNK))
					cinuse += CHUNK_HEADER_SIZE + inuse_size
				
			curr = next
		heaps.append(nodes)

	#Finding the bounds
	min_offset = min([min([curr for (curr, size, _) in heap]) for heap in heaps])
	scale_factor = 0.5

	#Rendering the heaps to an HTML file
	output_file = open(output_file_path, "w")
	output_file.write("<html>\n")
	output_file.write("  <body>\n")
	output_file.write("    <div id=\"container\">");

	for idx, heap in enumerate(heaps):
		output_file.write("\n")
		top = (RENDER_HEIGHT + SPACER_HEIGHT)*idx + RENDER_HEIGHT
		output_file.write("\n".join(["        " +  generate_chunk_div(curr, size, min_offset, top, type) for (curr,size,type) in heap]))

	output_file.write("\n")	
	output_file.write("    </div>\n")
	output_file.write("  </body>\n")
	output_file.write("</html>\n")
	output_file.close()

if __name__ == "__main__":
	main()
