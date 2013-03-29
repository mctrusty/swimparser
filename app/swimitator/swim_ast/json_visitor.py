from swim_visitor import SwimAstVisitor
from node import xstr

class SwimJsonVisitor(SwimAstVisitor):
    """
    Base class for visitor that processes language parsed by the
    swimitator swim_parser.
    """
    def visit_workout(self, node):
        node.json = '{'
        
    def visit_setlist(self, node):
        node.json = '"setlist": ['

    def visit_set(self, node):
        node.json = '{'

    def visit_multiset(self, node):
        node.json = '{"reps": ' + str(node.repeats) + ', '

    def visit_count(self, node):
        node.json = ''

    def visit_reps(self, node):
        node.json = '"reps": '  + xstr(node.reps) + ', '
        
    def visit_distance(self, node):
        node.json = '"distance": ' + xstr(node.distance) + ', '
        
    def visit_stroke(self, node):
        if node.stroke:
            node.json = '"stroke": "' + xstr(node.stroke) + '", '
        else:
            node.json = '"stroke": null, '

    def visit_zone(self, node):
        if node.zone:
            node.json = '"zone": "' + xstr(node.zone) + '",'
        else:
            node.json = '"zone": null, '
                    
    def visit_interval(self, node):
        node.json = '"time": ' + xstr(node.minutes * 60 + node.seconds)

    def visit_kick(self, node):
        node.json = '"skill": "kick",'
            
    def visit_drill(self, node):
        node.json = '"skill" : drill,'
                

class SwimJsonCloseVisitor(SwimAstVisitor):
    """
    Provides closing tags for xml elements that require them.
    """
    def visit_workout(self, node):
        node.json = '}'
        
    def visit_set(self, node):
        node.json = "}, "

    def visit_setlist(self, node):
        node.json = "]"

    def visit_multiset(self, node):
        node.json = "}"
