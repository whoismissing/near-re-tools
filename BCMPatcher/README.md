https://project-zero.issues.chromium.org/42450052#attachment59035508

inline firmware patcher.

 - [patch.py](./patch.py) : The patcher itself.
 - apply_* : Scripts to apply each of the patches using dhdutil
 - <DEV>/BCMFreePatch : Patch for the "free" function in the firmware
 - <DEV>/BCMMallocPatch : Patch for the "malloc" function in the firmware
 - <DEV>/BCMDumpMPU : Patch that dumps the MPU's contents
