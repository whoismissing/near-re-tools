import sys, struct, re, os

#The height of each rendered block
RENDER_HEIGHT = 30

#The height of the space between rows
SPACER_HEIGHT = 10

#The horizontal scale factor
SCALE_FACTOR = 0.5

#The type of chunk to be presented
FREE_CHUNK = 0
INUSE_CHUNK = 1

#The types of sanitised log events
MALLOC = 0
FREE = 1
MALLOC_RES = 2

def generate_chunk_div(curr, size, min_offset, top, type):
	color = 'gray' if type == FREE_CHUNK else 'red'
        style = ("".join(["style=\"position: absolute; ",
                          "border: 1px solid black; ",
                          "opacity: 0.75;",
                          "left: %f;",
                          "top: %d;",
                          "width: %f;",
                          "height: %d;",
                          "background: %s;\""])) % ((curr - min_offset) * SCALE_FACTOR, top, size * SCALE_FACTOR, RENDER_HEIGHT, color)
	title = "title=\"0x%08X , size: 0x%X\"" % (curr, size)
	return "<div %s %s></div>" % (style, title)

def main():

	#Reading the agruments
	if len(sys.argv) < 3:
		print "USAGE: %s <TRACE_FILE> <OUTPUT_FILE>" % sys.argv[0]
		return
	trace_file_path = sys.argv[1]
	output_file_path = sys.argv[2]

        #Reading the events from the trace file
        events = []
        for line in open(trace_file_path, 'r').readlines():
            m = re.match("^\\((\\d+)\\) malloc - size: ([\\d]+), caller: ([0-9a-f]+), res: ([0-9a-f]+)\\s*$", line)
            if m:
                events.append((int(m.group(1)), MALLOC, int(m.group(4), 16), int(m.group(2))))
                continue
            m = re.match("^\\((\\d+)\\) free - ptr: ([0-9a-f]+)\\s*$", line)
            if m:
                events.append((int(m.group(1)), FREE, int(m.group(2), 16)))
                continue

	#Finding the bounds
	min_offset = min([event[2] for event in events])
	scale_factor = 0.5

	#Rendering the trace to an HTML file
	output_file = open(output_file_path, "w")
	output_file.write("<html>\n")
	output_file.write("  <body>\n")
	output_file.write("    <div id=\"container\">");

	#Going over each event and rendering it into the HTML file
	heap = []

	for idx, event in enumerate(events):

		if event[1] == MALLOC:
			heap.append([event[2], event[3], INUSE_CHUNK])
		elif event[1] == FREE:
			#Searching for this block
			for chunk in heap:
				if chunk[0] == event[2]:
					chunk[2] = FREE_CHUNK
					break
		
		#Rendering the heap state
		output_file.write("\n")
		top = (RENDER_HEIGHT +SPACER_HEIGHT)*idx + RENDER_HEIGHT	
		output_file.write("\n".join(["        " +  generate_chunk_div(curr, size, min_offset, top, type) for (curr,size,type) in heap]))

	output_file.write("\n")	
	output_file.write("    </div>\n")
	output_file.write("  </body>\n")
	output_file.write("</html>\n")
	output_file.close()

if __name__ == "__main__":
	main()
