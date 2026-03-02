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

pre:
    #Calling the pre-hook
    PUSH {R0-R11}
    LDR R6, counter_address
    LDR R1, [R6]
    ADD R1, R1, #1
    STR R1, [R6]
    LDR R5, printf
    MOV R2, R0
    MOV R3, LR
    ADR R0, preformatstr
    BLX R5
    POP {R0-R11}

call_func:
    #Calling the function itself (first emulating the replaced
    #opcodes, then jumping to the rest of the function).
    BLX run_func

post:

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
preformatstr:
    .asciz "%d f p %x c %x\n"

.code 16
.align 4
run_func:
    NOP
