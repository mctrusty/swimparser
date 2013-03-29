from Node import *

class SwimAstVisitor():
    """
    Base class for visitor that processes language parsed by the
    swimitator swim_parser.
    """

    def visit(self, node):
        """
        Visit the base Node instance.
        """
       # if node.type: #output node type for debugging purposes
       #     print "visiting " + node.type

#dispatch node to its proper visitor type
        if isinstance(node, Set):
            self.visit_set(node)
        if isinstance(node, SetList):
            self.visit_setlist(node)
        if isinstance(node, MultiSet):
            self.visit_multiset(node)
        if isinstance(node, Count):
            self.visit_count(node)
        if isinstance(node, Interval):
            self.visit_interval(node)
        if isinstance(node, Zone):
            self.visit_zone(node)
        if isinstance(node, Kick):
            self.visit_stroke(node)
        if isinstance(node, Drill):
            self.visit_drill(node)
        if isinstance(node, Stroke):
            self.visit_stroke(node)
            
    def visit_set(self, node):
        pass

    def visit_setlist(self, node):
        pass

    def visit_multiset(self, node):
        pass

    def visit_count(self, node):
        pass

    def visit_interval(self, node):
        pass

    def visit_zone(self, node):
        pass

    def visit_kick(self, node):
        pass

    def visit_drill(self, node):
        pass

    def visit_stroke(self, node):
        pass
