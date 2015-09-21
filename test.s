.globl main
main:
	pushl %ebp
	movl %esp, %ebp
	subl $24, %esp
	call input
	movl %eax, -0x4(%ebp)
	addl $5, -0x4(%ebp)
	movl $6, %edx
	negl %edx
	movl %edx, -0x8(%ebp)
	movl -0x8(%ebp), %edx
	addl -0x4(%ebp), %edx
	movl %edx, -0x12(%ebp)
	call input
	movl %eax, -0x16(%ebp)
	movl -0x16(%ebp), %edx
	addl -0x12(%ebp), %edx
	movl %edx, -0x20(%ebp)
	movl -0x20(%ebp), %edx
	movl %edx, -0x24(%ebp)
	addl $24, %esp
	movl $0, %eax
	leave
	ret
