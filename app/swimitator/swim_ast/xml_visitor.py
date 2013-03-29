from swim_visitor import SwimAstVisitor
from node import xstr

class SwimXmlVisitor(SwimAstVisitor):
    """
    Base class for visitor that processes language parsed by the
    swimitator swim_parser.
    """

    def visit_workout(self, node):
        node.xml = ''
        
    def visit_set(self, node):
        node.xml = "<set>"

    def visit_setlist(self, node):
        node.xml = "<setlist xmlns=\"http://swimparser.appspot.com/xml\">"

    def visit_multiset(self, node):
        node.xml = "<multiset><reps>" + str(node.repeats) + "</reps>"

    def visit_count(self, node):
        node.xml = '<count>'

    def visit_reps(self, node):
        node.xml = "<reps>" + xstr(node.reps) + "</reps>" 
        
    def visit_distance(self, node):
        node.xml = "<distance>" + xstr(node.distance) + "</distance>"
        
    def visit_interval(self, node):
        node.xml = "<time>" + xstr(node.minutes * 60 + node.seconds) + "</time>"

    def visit_zone(self, node):
        node.xml = "<zone>" + xstr(node.zone) + "</zone>"

    def visit_kick(self, node):
        node.xml = "<skill>kick</skill>"

    def visit_drill(self, node):
        node.xml = "<skill>drill</skill>"

    def visit_stroke(self, node):
        node.xml = "<stroke>" + xstr(node.stroke) + "</stroke>"
                
    
class SwimXmlCloseVisitor(SwimAstVisitor):
    """
    Provides closing tags for xml elements that require them.
    """
    def visit_workout(self, node):
        node.xml = ''
        
    def visit_set(self, node):
        node.xml = "</set>"

    def visit_setlist(self, node):
        node.xml = "</setlist>"

    def visit_multiset(self, node):
        node.xml = "</multiset>"
        
    def visit_count(self, node):
        node.xml = '</count>'
