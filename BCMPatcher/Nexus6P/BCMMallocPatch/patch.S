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
    PUSH {LR}

call_func:
    #Calling the function itself (first emulating the replaced
    #opcodes, then jumping to the rest of the function).
    PUSH {R0, LR}
    BLX run_func

post:

    #Busy looping to slow us down a little, letting the host
    #extract the console dump before it vanishes
    PUSH {R0,R1}
    MOV R0, #0
    MOV R1, #0x100000
loop:
    CMP R0, R1
    BEQ endloop
    ADD R0, R0, #1
    B loop
endloop:
    POP {R0, R1}

    #Running the post hook after the function returns
    POP {R2, R3}
    PUSH {R0-R11}
    LDR R6, counter_address
    LDR R1, [R6]
    ADD R1, R1, #1
    STR R1, [R6]
    LDR R5, printf
    MOV R4, R0
    ADR R0, formatstr
    BLX R5
    POP {R0-R11}

ret_to_caller:
    #Returning to the original caller
    POP {LR}
    BX LR

.align 4
printf:
    .word 0x374D

.align 4
counter_address:
    .word 0x180050

.align 4
formatstr:
    .asciz "%d m s %d c %x r %x\n"

.code 16
.align 4
run_func:
    NOP
