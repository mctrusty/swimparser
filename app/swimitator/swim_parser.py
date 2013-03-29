# /usr/bin/python

# Copyright 2013 Michael J. Cox

"""
Parses a shorthand language often used to notate swimming
workouts.

It uses David Beazley's PLY lex/yacc libraries.

**parser**: parser object loaded with the swim language.
"""
from ply import lex
from ply import yacc
from swim_lexer import tokens
from swim_ast.node import *

precedence = (
	('nonassoc', 'R_BRACKET'),
	('nonassoc', 'NUMBER'),
)

def p_workout_or_empty(p):
	"""
	workout : 
				| set_list
	"""
	if len(p) == 2:
		p[0] = Workout(p[1])
	else:
		raise Exception('Empty Input')
	
def p_workout(p):
        """
		set_list : set_list set %prec NUMBER
        set_list : set_list multi_set %prec NUMBER
	"""

	p[0] = p[1].add_set(p[2])

def p_set_list(p):
	"""
		set_list : set %prec NUMBER
					| multi_set %prec NUMBER
	"""
	p[0] = SetList(p[1])

def p_super_set(p):
        """
        multi_set : NUMBER MULT L_BRACKET set_list R_BRACKET
        """

        p[0] = MultiSet(p[4],p[1])

def p_set(p):
	"""
	set : count skill zone interval
	"""
	if len(p) == 1:
		p[0] = []
	else:
		p[0] = Set([p[1] ,p[2], p[3],p[4]])
        
def p_empty(p):
	'empty :'
	pass
	
def p_count(p):
	"""
	count : NUMBER
	      | NUMBER MULT NUMBER
	"""
	if len(p) == 1:
		print 'No start token'
	if len(p) == 2:
		p[0] = Count(1,p[1])
	elif len(p) == 4:
		p[0] = Count(p[1] ,p[3])

def p_skill_stroke(p):
	"""
	skill : empty 
	      | STROKE
	"""
	if len(p) == 2:
		p[0] = Stroke(p[1])
	else:
		p[0] = Stroke('choice')
		
def p_skill_drill(p):
	"""
	skill : DRILL
	      | STROKE DRILL
	"""
	if len(p) == 3:
		p[0] = Drill(p[1],p[2])
	else:
		p[0] = Drill('choice',p[1])

def p_skill_kick(p):
	"""
	skill : KICK
	      | STROKE KICK
	"""
	if len(p) == 3:
		p[0] = Kick(p[1])
	else:
		p[0] = Kick('choice')
		
def p_zone(p):
	"""
	zone : ZONE
	     | empty
	"""
	if len(p)==2:
		p[0] = Zone(p[1])
	else:
		p[0] = 'none'
	
def p_interval(p):
	"""
	interval : AT NUMBER COLON NUMBER
		 | AT NUMBER
		 | empty
	"""
	if len(p) == 5:
		p[0] = Interval(p[2],p[4])
	elif len(p) == 3:
		p[0] = Interval(0,p[2])
	else:
		p[0] = Interval(0,0)
		
def p_error(p):
        if p == None:
                print "missing token"
                raise TypeError("Token Missing")
        else:
                print "Syntax error at token, unexpected", p.type, "on line", str(p.lineno)
#	raise TypeError("Unknown Text '%s'" % (p.type))               
        yacc.errok()

parser = yacc.yacc(debug=False)

if __name__ == "__main__":
        import logging
        logging.basicConfig(
                level = logging.DEBUG,
                filename="parselog.txt",
                filemode="w",
                format="%(filename)10s:%(lineno)4d:%(message)s",
        )
        log = logging.getLogger()

        while True:
                try: 
                        s = raw_input('set>')
                except EOFError:
                        break
                if not s: continue
                if s=='q':
                        break
                result = parser.parse(s,debug=log)
                print result
	
