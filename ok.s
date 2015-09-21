.globl main
main:
	pushl %ebp
	movl %esp, %ebp
	movl $1, %edx
	addl $2, %edx
	pushl %edx
	call print_int_nl
	addl $0, %esp
	movl $0, %eax
	leave
	ret
