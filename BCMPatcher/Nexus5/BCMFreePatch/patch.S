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
    ADR R0, preformatstr
    BLX R5
    POP {R0-R11}

call_func:
    POP {LR}
    MOV R0, R1
    CMP R1, #0
    BEQ ret
    LDR PC, free
ret:
    BX LR

.align 4
printf:
    .word 0x126F1

.align 4
preformatstr:
    .asciz "free, addr: %x\n"

.align 4
free:
    .word 0x16621
