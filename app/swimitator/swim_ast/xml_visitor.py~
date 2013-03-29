from swim_ast_visitor import SwimAstVisitor
from Node import xstr

class SwimXmlVisitor(SwimAstVisitor):
    """
    Base class for visitor that processes language parsed by the
    swimitator swim_parser.
    """
            
    def visit_set(self, node):
        print "<set>"

    def visit_setlist(self, node):
        print "<setlist>"

    def visit_multiset(self, node):
        print "<multiset>"
        print "<reps>" + str(node.repeats) + "<\reps>"

    def visit_count(self, node):
        print "<reps>" + xstr(node.reps) + "</reps>" + "<distance>" + xstr(node.distance) + "</distance>"

    def visit_interval(self, node):
        print "<time>" + xstr(node.minutes * 60 + node.seconds) + "</time>"

    def visit_zone(self, node):
        print "<zone>" + xstr(node.zone) + "</zone>"

    def visit_kick(self, node):
        print "<skill>kick</skill>"

    def visit_drill(self, node):
        print "<skill>drill</skill>"

    def visit_stroke(self, node):
        print "<stroke>" + xstr(node.stroke) + "</stroke>"
                
    
class SwimXmlCloseVisitor(SwimAstVisitor):
    """
    Provides closing tags for xml elements that require them.
    """

    def visit_set(self, node):
        print "</set>"

    def visit_setlist(self, node):
        print "</setlist>"

    def visit_multiset(self, node):
        print "</multiset>"
