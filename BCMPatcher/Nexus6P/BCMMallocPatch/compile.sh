#!/bin/bash
BIN_PATH=/path/to/your/arm/eabi
$BIN_PATH/as patch.S -o patch.o
$BIN_PATH/objcopy -O binary patch.o patch.bin
$BIN_PATH/objdump -D patch.o
