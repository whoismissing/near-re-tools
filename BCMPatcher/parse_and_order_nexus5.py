import sys, os, re

MALLOC = 0
FREE = 1
MALLOC_RES = 2

MAX_ADDRESS = 0x300000

def main():
    
    #Parsing the commandline arguments
    if len(sys.argv) != 3:
        print "USAGE: %s <LOG_FILE> <OUTPUT_FILE>"
        return
    log_file_path, output_file_path = sys.argv[1:]

    #First running sort & uniq
    os.system("sort %s | uniq > %s" % (log_file_path, output_file_path))

    #Now, going over each line and making sure it fits the format for a dump file
    f = open(output_file_path, "r")
    lines = f.read().split("\n")
    f.close()
    events = []
    for line in lines:
        m = re.match("^(\\d{6}\\.\\d{3}) malloc, size: (\\d+), caller: ([0-9a-f]+)\s*$", line)
        if m:
            if int(m.group(3), 16) > MAX_ADDRESS:
                continue #Rejecting possibly malformed event
            events.append((float(m.group(1)), MALLOC, int(m.group(2)), int(m.group(3), 16)))
            continue
        m = re.match("^(\\d{6}\\.\\d{3}) malloc, res: ([0-9a-f]+)\s*$", line)
        if m:
            if int(m.group(2), 16) > MAX_ADDRESS:
                continue #Rejecting possibly malformed event
            events.append((float(m.group(1)), MALLOC_RES, int(m.group(2), 16)))
            continue
        m = re.match("^(\\d{6}\\.\\d{3}) free, addr: ([0-9a-f]+)\s*$", line)
        if m:
            if int(m.group(2), 16) > MAX_ADDRESS:
                continue #Rejecting possibly malformed event
            events.append((float(m.group(1)), FREE, int(m.group(2), 16)))
            continue
        m = re.match("^(\\d{6}\\.\\d{3}) free, ptr: ([0-9a-f]+), caller: ([0-9a-f]+)\s*$", line)
        if m:
            if int(m.group(2), 16) > MAX_ADDRESS:
                continue #Rejecting possibly malformed event
            events.append((float(m.group(1)), FREE, int(m.group(2), 16)))
            continue
    
    f = open(output_file_path, "w")
    for event in events:
        if event[1] == MALLOC:
            f.write("(%04f) malloc - size: %d, caller: %x\n" % (event[0], event[2], event[3]))
        elif event[1] == FREE:
            f.write("(%04f) free - ptr: %x\n" % (event[0], event[2]))
        elif event[1] == MALLOC_RES:
            f.write("(%04f) malloc - res: %x\n" % (event[0], event[2]))

if __name__ == "__main__":
    main()
