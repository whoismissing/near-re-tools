#!/bin/bash


#Setting the counter to zero
python -c "from patch import *; print write_dword(0x180050, 0);"

#Both of the patches are currently just stored at the start of the heap
#(under the assumption allocations never actually reach those addresses).
#Eventually this should probably be properly carved (i.e., reducing the
#size of the free chunk and fixing the pointer in the prev chunk)
python patch.py 0x18222C 0x1E8C30 Nexus6P/BCMFreePatch/patch.bin
python patch.py 0x182118 0x1E8F30 Nexus6P/BCMMallocPatch/patch.bin
