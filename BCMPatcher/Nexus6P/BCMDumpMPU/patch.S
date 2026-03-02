.code 16
hook_thumb:
    #Switching to ARM
    PUSH {R0}
    ADR R0, hook_arm
    BX R0

.code 32
.align 4
hook_arm:

    POP {R0}
    PUSH {R0-R11, LR}

    ADR R0, markstr
    LDR R4, printf
    BLX R4

    MOV R5, #12 //number of MPU regions
    MOV R6, #0
loop:
    CMP R6, R5
    BGE end_loop
    
    //Setting the region number register
    MCR p15, 0, R6, c6, c2, 0

    //Reading the region data
    MRC p15, 0, R1, c6, c1, 0 //base address
    MRC p15, 0, R2, c6, c1, 2 //size & enable
    MRC p15, 0, R3, c6, c1, 4 //access control
    ADR R0, formatstr
    LDR R4, printf
    BLX R4
    ADD R6, R6, #1
    b loop
        
end_loop:
    POP {R0-R11, LR}
    LDR PC, ioctl

.align 4
ioctl:
    .word 0x19735

.align 4
printf:
    .word 0x374D

.align 4
formatstr:
    .asciz "rg %08x %08x %08x\n"

.align 4
markstr:
    .asciz "------\n"
