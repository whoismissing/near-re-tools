import sys, os, re

MALLOC = 0
FREE = 1

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
        m = re.match("^\\d{6}\\.\\d{3} (\d+) m s (\\d+) c ([0-9a-f]+) r ([0-9a-f]+)\s*$", line)
        if m:
            if int(m.group(3), 16) > MAX_ADDRESS:
                continue #Rejecting possibly malformed event
            events.append((float(m.group(1)), MALLOC, int(m.group(2)), int(m.group(3), 16), int(m.group(4), 16)))
            continue
        m = re.match("^\\d{6}\\.\\d{3} (\d+) f p ([0-9a-f]+) c ([0-9a-f]+)\s*$", line)
        if m:
            if int(m.group(2), 16) > MAX_ADDRESS:
                continue #Rejecting possibly malformed event
            events.append((float(m.group(1)), FREE, int(m.group(2), 16)))
            continue
    events = sorted(set(events))


    f = open(output_file_path, "w")
    for event in events:
        if event[1] == MALLOC:
            f.write("(%d) malloc - size: %d, caller: %x, res: %x\n" % (event[0], event[2], event[3], event[4]))
        elif event[1] == FREE:
            f.write("(%d) free - ptr: %x\n" % (event[0], event[2]))

if __name__ == "__main__":
    main()
