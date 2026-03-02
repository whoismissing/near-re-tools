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
    LDR R5, printf
    MOV R1, R0
    MOV R2, LR
    ADR R0, preformatstr
    BLX R5
    POP {R0-R11}

call_func:
    #Calling the function itself (first emulating the replaced
    #opcodes, then jumping to the rest of the function).
    BLX run_func

post:
    #Running the post hook after the function returns
    PUSH {R0-R11}
    LDR R5, printf
    MOV R1, R0
    ADR R0, postformatstr
    BLX R5
    POP {R0-R11}

ret_to_caller:
    #Returning to the original caller
    POP {LR}
    BX LR

.align 4
printf:
    .word 0x126F1

.align 4
preformatstr:
    .asciz "malloc, size: %d, caller: %x\n"

.align 4
postformatstr:
    .asciz "malloc, res: %x\n"

.code 16
.align 4
run_func:
    NOP
