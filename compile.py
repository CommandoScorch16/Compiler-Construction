import compiler
import sys


from compiler.ast import *


#x86 classes

class add(Node):
	def __init__(self,left,right):
		for x in range(1,6):
			if (arrOfRegisters1[x].name == right):
				arrOfRegisters1[x].isInUse = 0
		
		self.left = left
		self.right = right
		
		
	def printl(self):
		print ('add(%s, %s)' % (self.left, self.right))
        

class neg(Node):
	def __init__(self,value):
		self.value = value
		#print ('neg(%s)' % (self.value))

	def printl(self):
		print ('neg(%s)' % (self.value))

class printl(Node):
	def __init__(self, expr):
		self.expr = expr

class push(Node):
	def __init__(self, expr):
		
		for x in range(1,6):
			if (arrOfRegisters1[x].name == expr):
				arrOfRegisters1[x].isInUse = 0
		
		if isinstance(expr, Const):
			self.expr = '$'+str(expr.value)

		elif isinstance(expr, Name):
			v = varExists(expr.name)
			if v != 'false':
				self.expr = v
				
		else:
			self.expr = expr

class assign(Node):
	def __init__(self,a,value):

		for x in range(1,6):
			if (arrOfRegisters1[x].name == a):
				arrOfRegisters1[x].isInUse = 0
				


		if (isInArrOfVarLocs(a) == 'true' and (a == value)):
			self.a = 'The Old GraY Goosed is Dead'
			self.value = 'The Old GraY Goosed is Dead'
			
		elif (isInArrOfVarLocs(a) == 'true' and isInArrOfVarLocs(value) == 'true'):
			c = createNewVar()
			happy = assign(a, c)
			listOfInstructions.append(happy)
			happy = assign(c, value)
			listOfInstructions.append(happy)
			self.a = 'The Old GraY Goosed is Dead'
			self.value = 'The Old GraY Goosed is Dead'
		
		elif isinstance(a, Const):
			self.a = '$'+str(a.value)
			self.value = value
					
		else:
			self.a = a
			self.value = value
				
		#self.a = a
		#self.value = value
		#print ('assign(%s, %s)' % (self.a, self.value))
		
	
        #print ('assign(%s, %s)' % (self.a, self.value))
	
class call(Node):
	def __init__(self,a,b):
		global amountToSub
		self.a = a
		self.b = b
		for x in range (0, len(b)):
			if isinstance(b[x], Const):
				b[x] = b[x].value
			elif isinstance(b[x], Name):
				b[x] = flattenAST(b[x])
	



#end x86 classes


class register(Node):
	def __init__(self, name, isInUse):
		self.name = name
		self.isInUse = isInUse


currentNumber = 0
happy = 0
counter = 0
listOfInstructions = []
arrOfRegisters = ['%eax', '%edx', '%ebx', '%esi', '%edi', '%ecx']
qOfRegisters = ['%eax', '%edx', '%ebx', '%esi', '%edi', '%ecx']

arrOfRegisters1 = []
qOfRegisters1 = []

currentNumberOfVars = 0
arrOfVars = []
arrOfVarLocs = []

for x in range(0,6):
	arrOfRegisters1.append(register(arrOfRegisters[x], 0))
	qOfRegisters1.append(register(qOfRegisters[x], 0))


listOfVars = []
amountToSub = 0
fo = open("out.s", "w+")

def isInArrOfVarLocs(var):
	k = 'false'

	for i in range(0, len(arrOfVarLocs)):
		if arrOfVarLocs[i] == var:
			k = 'true'
	return k

def varExists(var):
	if (isinstance(var, Name)):
		var = var.name
		
	for x in range (0, len(arrOfVars)):
		if arrOfVars[x] == var:
			return arrOfVarLocs[x]

	return 'false'

currentNumberOfTemps = 0
def createTempVar():
	global currentNumberOfTemps
	global amountToSub
	currentNumberOfTemps += 1
	return str(currentNumberOfTemps)

def createVar(var):
	global arrOfVars
	global arrOfVarLocs
	global currentNumberOfVars
	arrOfVars.append(var)
	currentNumberOfVars += 1
	arrOfVarLocs.append('-0x'+(str(4*currentNumberOfVars)+('(%ebp)')))
	return arrOfVarLocs[currentNumberOfVars-1]

def checkVar(name, place):
	place1 = 0
	for x in range(0,len(arrOfVars)):
		if (arrOfVars[x] == name):
			if (arrOfVarLocs[x] != place):
				return 'false'
			else:
				return 'true'

def getPlace(var):
	for x in range(0,len(arrOfVars)):
		return

def howdy():
	a = [1, 2, 3]
	for i in range (0, len(a)):
		a[i] = 4
	#print a
    

def createNewVar():
	global currentNumber
	global arrOfRegisters1

	for x in range(1,6):
		if arrOfRegisters1[x].isInUse == 0:
			arrOfRegisters1[x].isInUse = 1
			return arrOfRegisters1[x].name
		
	currentNumber = currentNumber+1
	return #listOfVars[currentNumber-1]#return 'tmp%d' % (currentNumber,)

def createSetVar(num):
	return arrOfRegisters[currentNumber-1]#return 'tmp%d' % (currentNumber,)











def flattenAST(ast):

	if isinstance(ast, Module):
		return flattenAST(ast.node)

	if isinstance(ast, Stmt):
		for x in ast.nodes:
			j = flattenAST(x)

	if isinstance(ast, Discard):
		j = flattenAST(ast.expr)
		for x in range(1,6):
			if (arrOfRegisters1[x].name == j):
				arrOfRegisters1[x].isInUse = 0
		return j

	if isinstance(ast, Printnl):
		for x in ast.nodes:
			exp = flattenAST(x)
			happy = push(exp)
			listOfInstructions.append(happy)
			happy = printl(exp)
			listOfInstructions.append(happy)

	if isinstance(ast, Assign):
		for x in ast.nodes:
			if (isinstance(x, AssName)):
				v = flattenAST(x)
				b = flattenAST(ast.expr)
				if v != 'false':
					if (varExists(b) != 'false'):
						j = createNewVar()
						happy = assign(varExists(b), j)
						listOfInstructions.append(happy)
						happy = assign(j, v)
						listOfInstructions.append(happy)
						return j
						
					else:
						happy = assign(b, v)
						listOfInstructions.append(happy)
						return v

				else:
					j = createVar(x.name)
					d = varExists(b)
					if (d != 'false'):
						#print 'here'
						joy = createNewVar()
						happy = assign(d, joy)
						listOfInstructions.append(happy)
						happy = assign(joy, j)
						listOfInstructions.append(happy)
						return j
					
					else:
						#print 'really', b, j
						happy = assign(b, j)
						listOfInstructions.append(happy)
                           

	if isinstance(ast, UnarySub):
		j = flattenAST(ast.expr)
		if (isinstance(j, Name)):
			i = varExists(j.name)
			b = createNewVar()
			happy = assign(i, b)
			listOfInstructions.append(happy)
			happy = neg(b)
			listOfInstructions.append(happy)
			m = createVar(createTempVar())
			happy = assign(b, m)
			listOfInstructions.append(happy)
			return m
        
		elif (isinstance(j, Const)):
			b = createNewVar()
			j = '$'+str(j.value)
			happy = assign(j, b)
			listOfInstructions.append(happy)
			happy = neg(b)
			listOfInstructions.append(happy)
			m = createVar(createTempVar())
			happy = assign(b, m)
			listOfInstructions.append(happy)
			return m
        
		else:
			if (isInArrOfVarLocs(j) == 'true'):
				d = createNewVar()
				happy = assign(j, d)
				listOfInstructions.append(happy)
				happy = neg(d)
				listOfInstructions.append(happy)
				m = createVar(createTempVar())
				happy = assign(d, m)
				listOfInstructions.append(happy)
				return m
				
			else:
				happy = neg(j)
				listOfInstructions.append(happy)
				m = createVar(createTempVar())
				happy = assign(j, m)
				listOfInstructions.append(happy)
				return m

	if isinstance(ast, Add):
		l = flattenAST(ast.left)
		r = flattenAST(ast.right)
		if (isinstance(l, Name)):
			if (isinstance(r, Name)):
				d = createNewVar()
				j = createNewVar()
				happy = assign(varExists(r), d)
				listOfInstructions.append(happy)
				happy = assign(varExists(l), j)
				listOfInstructions.append(happy)
				happy = add(d, j)
				listOfInstructions.append(happy)
				return d
				
		   
			elif (isinstance(r, Const)):
					d = createNewVar()
					happy = assign(varExists(l), d)
					listOfInstructions.append(happy)
					happy = add(d, '$'+str(r.value))
					listOfInstructions.append(happy)
					return d
			
			elif (isinstance(r, CallFunc)):
				d = createNewVar()
				happy = assign(varExists(l), d)
				listOfInstructions.append(happy)
				happy = add(d, '$'+str(r.value))
				listOfInstructions.append(happy)
				j = createVar(createTempVar())
				happy = assign(d, j)
				listOfInstructions.append(happy)
				return j

			else:
				d = createNewVar()
				happy = assign(varExists(l), d)
				listOfInstructions.append(happy)
				happy = add(d, r)
				listOfInstructions.append(happy)
				return d
				
		elif (isinstance(l, Const)):
			if (isinstance(r, Name)):
				d = createNewVar()
				j = createNewVar()
				happy = assign('$'+str(l.value), d)
				listOfInstructions.append(happy)
				happy = assign(varExists(r.name), j)
				listOfInstructions.append(happy)
				happy = add(d, j)
				listOfInstructions.append(happy)
				return d
				
			elif (isinstance(r, Const)):
				d = createNewVar()
				happy = assign('$'+str(l.value), d)
				listOfInstructions.append(happy)
				happy = add(d, '$'+str(r.value))
				listOfInstructions.append(happy)
				return d
			
			elif (isinstance(r, CallFunc)):
				d = createNewVar()
				happy = assign(varExists(l), d)
				listOfInstructions.append(happy)
				happy = add(d, '$'+str(r.value))
				listOfInstructions.append(happy)
				j = createVar(createTempVar())
				happy = assign(d, j)
				listOfInstructions.append(happy)
				return j

			else:
				happy = add(r, '$'+str(l.value))
				listOfInstructions.append(happy)
				return r
			
		elif (isinstance(r, Name)):
			if (isinstance(l, Name)):
				d = createNewVar()
				j = createNewVar()
				happy = assign(varExists(l), d)
				listOfInstructions.append(happy)
				happy = assign(varExists(r), j)
				listOfInstructions.append(happy)
				happy = add(d, j)
				listOfInstructions.append(happy)
				return d
				
		   
			elif (isinstance(l, Const)):
					d = createNewVar()
					happy = assign(varExists(r), d)
					listOfInstructions.append(happy)
					happy = add(d, '$'+str(l.value))
					listOfInstructions.append(happy)
					return d
			
			elif (isinstance(l, CallFunc)):
				d = createNewVar()
				happy = assign(varExists(r), d)
				listOfInstructions.append(happy)
				happy = add(d, '$'+str(l.value))
				listOfInstructions.append(happy)
				j = createVar(createTempVar())
				happy = assign(d, j)
				listOfInstructions.append(happy)
				return j

			else:
				d = createNewVar()
				happy = assign(varExists(r), d)
				listOfInstructions.append(happy)
				happy = add(d, l)
				listOfInstructions.append(happy)
				return d
				
		elif (isinstance(r, Const)):
			if (isinstance(l, Name)):
				d = createNewVar()
				j = createNewVar()
				happy = assign('$'+str(r.value), d)
				listOfInstructions.append(happy)
				happy = assign(varExists(l.name), j)
				listOfInstructions.append(happy)
				happy = add(d, j)
				listOfInstructions.append(happy)
				return d
				
			elif (isinstance(l, Const)):
				d = createNewVar()
				happy = assign('$'+str(l.value), d)
				listOfInstructions.append(happy)
				happy = add(d, '$'+str(r.value))
				listOfInstructions.append(happy)
				return d
			
			elif (isinstance(l, CallFunc)):
				d = createNewVar()
				happy = assign(varExists(r), d)
				listOfInstructions.append(happy)
				happy = add(d, '$'+str(l.value))
				listOfInstructions.append(happy)
				j = createVar(createTempVar())
				happy = assign(d, j)
				listOfInstructions.append(happy)
				return j
			
			else:
				happy = add(l, '$'+str(r.value))
				listOfInstructions.append(happy)
				return l

		else:
			if (isInArrOfVarLocs(l) == 'true' and isInArrOfVarLocs(r) == 'true'):
				d = createNewVar()
				happy = assign(r, d)
				listOfInstructions.append(happy)
				happy = add(d, l)
				listOfInstructions.append(happy)
				j = createVar(createTempVar())
				happy = assign(d, j)
				listOfInstructions.append(happy)
				return j
			
			elif (isinstance(l, CallFunc)):
				d = createNewVar()
				happy = assign(varExists(r), d)
				listOfInstructions.append(happy)
				happy = add(d, '$'+str(l.value))
				listOfInstructions.append(happy)
				j = createVar(createTempVar())
				happy = assign(d, j)
				listOfInstructions.append(happy)
				return j
			
			elif (isinstance(r, CallFunc)):
				d = createNewVar()
				happy = assign(varExists(l), d)
				listOfInstructions.append(happy)
				happy = add(d, '$'+str(r.value))
				listOfInstructions.append(happy)
				j = createVar(createTempVar())
				happy = assign(d, j)
				listOfInstructions.append(happy)
				return j
			
			else:
				happy = add(l, r)
				listOfInstructions.append(happy)
				return l
			
		

	if isinstance(ast, AssName):
		return varExists(ast.name)

	if isinstance(ast, CallFunc):
		if (ast.node.name == 'input'):
			happy = call('input', ast.args)
			listOfInstructions.append(happy)
			j = createVar(createTempVar())
			happy = assign('%eax', j)
			listOfInstructions.append(happy)
			return j

	if isinstance(ast, Const):
		return ast

	if isinstance(ast, Name):
		return ast


def getAssembly(exp):
	global arrOfRegisters

	if isinstance(exp, add):
		fo.write('	addl %s, %s\n' % (exp.right, exp.left, ))

	elif isinstance(exp, assign):
		if (exp.a == 'The Old GraY Goosed is Dead' and exp.value == 'The Old GraY Goosed is Dead'):
			return

		else:
			if (isinstance(exp.value, call)):
				exp.value = '%eax'
				
			fo.write('	movl %s, %s\n' % (exp.a, exp.value, ))

	elif isinstance(exp, neg):
		fo.write('	negl %s\n' % (exp.value,))

	elif isinstance(exp, call): 
		fo.write('	call %s\n' % (exp.a, ))

	elif isinstance(exp, push):
		fo.write('	pushl %s\n' % (exp.expr))

	elif isinstance(exp, printl):
		fo.write('	call print_int_nl\n')


def start(argv):
	global fo
	howdy = ''
	happyier = ''

	for x in argv[1]:
		if (x != '.'):
			howdy+=x
			happyier+=x
		else:
			break

	happyier += '.in'
	
	#with open(argv[1]) as f:
	#	for line in f:
	#		line = line.split('#', 1)[0]
	#		line = line.rstrip()
	f = open(argv[1])
	text = f.read()
	f.close()
	#ast = parser.parser.parse(text)
	ast = compiler.parseFile(argv[1])
	#ast = compiler.parseFile('wow.py')
	#ast = compiler.parse('a = 5 + input() +-6 + input()')
	fo = open(howdy + '.s', 'w+')
	#line = fo.write( 'Howdy Charlie\n' )
	#fo.write('hi\n')
	#print 'happy'
	flattenAST(ast)
	global amountToSub
	global currentNumberOfVars
	amountToSub = 4*currentNumberOfVars
	#print ('\nAssembly:')
	fo.write('.globl main\n')
	fo.write('main:\n')
	fo.write ('	pushl %ebp\n')
	fo.write ('	movl %esp, %ebp\n')
	if (amountToSub > 0):
		fo.write (('	subl $%s,' % (amountToSub,))+' %esp\n')
		
	for x in listOfInstructions:
		getAssembly(x)
	fo.write (('	addl $%s,' % (amountToSub,))+' %esp\n')
	fo.write ('	movl $0, %eax\n')
	fo.write ('	leave\n')
	fo.write ('	ret\n')

start(sys.argv)
