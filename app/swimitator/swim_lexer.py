# coding: utf-8
# swim_lexer tokenizes a shorthand language often used to notate swimming workouts
# it uses David Beazley's PLY parser to do the lexing 
# @author: Michael J. Cox

from ply import lex

tokens = (
    "L_BRACKET",
    "R_BRACKET",
    "KICK",
    "DRILL",
    "STROKE",
    "NUMBER",
    "MULT",
    "COLON",
    "AT",
    "ZONE"
)

t_ignore = ' \t'

def t_newline(t):
    r"\n|\r\n"
    t.lexer.lineno += len(t.value)
    
t_AT = (r"@")

t_L_BRACKET = ( r"{")

t_R_BRACKET = ( r"}")

t_COLON = (r":")

t_MULT = (
    r"x|X"
)

t_KICK = ( r"[Kk](ick)?")

t_DRILL = ( r"[Dd]r(ill)?")

t_STROKE = ( r"[Cc]h(oice)?|[Ff]ly?|[Bb]r(east)?|[Bb](a|k)(ck)?|[Ff]r(ee)?|[Ii][Mm]")

t_ZONE = (
    r"(EN|[Zz](one|ONE)?)\s?\d+"
)

def t_NUMBER(t):
    r"\d+"
    t.value=int(t.value)
    return t

def t_error(t):
    raise TypeError("Unknown text '%s'" % (t.value,))
    
lexer = lex.lex()

'''
Helper methods
-----------------------
'''
def dump_tokens(w):
    """Return a string of tokens for a given input string.
        
        params:
        w - workout string
        
    """
    out = []
    lexer.input(w)
    while True:
        tok = lexer.token()
        if not tok: break
        out.append(tok.type)
    return ' '.join(out)

def dump_token_info(w):
    """Return a list of LexTokens for a given input string.
        
        params:
        w - workout string
        
    """
    out = []
    lexer.input(w)
    while True:
        tok = lexer.token()
        if not tok: break
        out.append(tok)
    return out

'''
-----------------------
Helper methods
'''
if __name__ == "__main__":
    import sys
    if not len(sys.argv) == 2:
        print "usage swim_lexer workout"
    else:
        print dump_tokens(sys.argv[1])
