#!/bin/bash
#Both of the patches are currently just stored at the start of the heap
#(under the assumption allocations never actually reach those addresses).
#Eventually this should probably be properly carved (i.e., reducing the
#size of the free chunk and fixing the pointer in the prev chunk)
python patch.py 0x184F04 0x1EBE8C Nexus5/BCMFreePatch/patch.bin
python patch.py 0x1814F4 0x1EC18C Nexus5/BCMMallocPatch/patch.bin
