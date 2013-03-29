#!/usr/bin/python

# Copyright 2013 Michael J. Cox

"""
A set of Node classes for representing parts of "swim workout" notation.
"""

def xstr(s):
        """
        Returns an empty string if the string passed in NoneType.
        """
        return '' if s is None else str(s)

class Node():
    """
    Base class for swim AST.
    """
    children = []
    
    def __init__(self, data):
        self.data = data
        self.children = []
    
    def add_child(self, obj):
        self.children.append(obj)
    
    def accept(self, visitor):
        visitor.visit(self)
    
    def xstr(self, s):
        """
        Returns an empty string if the string passed in NoneType.
        """
        return '' if s is None else str(s)
        pass

class Workout(Node):
    """
    Contains list of sets that comprise a workout.
    """
    def __init__(self, child=None):
        self.type = "workout"
        if child:
            self.children= [child]
        else:
            self.children = []

class SetList(Node):
    """
    Contains list of sets

    """
    def __init__(self, child=None, repeats=1):
        self.type = "set_list"
        if child:
            self.children= [child]
        else:
            self.children = []
        self.repeats = repeats
        self.data = repeats

    def add_set(self, set):
        self.children.append(set)
        return self

    def get_all_sets(self):
        return self.children

class MultiSet(Node):
    """
    Contains a set of sets, for when you want to iterate over a
    series of sets mutliple times.

    Example::

        3 x {
            2 x 50 freestyle EN1 @45
            3 x 100 K EN3 @2
        }

    """
    def __init__(self, child, repeats=1):
        self.type = "multi_set"
        if child:
            self.children = [child]
        else:
            self.children = []
        self.repeats = repeats
        self.data = repeats

class Set(Node):
    """
    The basic representation of one unit of work in a swimming
    workout. It describes number of reps, distance, stroke, skill,
    intensity level, and interval

    Example::

        10 x 100 fly EN3 @2:00

    """
    def __init__(self, children=None, leaf=None):
        self.type = "set"
        if children:
            self.children = children
        else:
            self.children = []
        self.leaf = leaf
        self.data = leaf
        
    #def __repr__(self):
    #    return self.children

class Count(Node):
    """
    Tracks information on number of reps and distance of those
    reps for a Set.

    Example::

        5 x 50

    """
    def __init__(self, reps, value):
        self.type = "count"
        self.reps = reps
        self.distance = value
        self.data = {'reps' : reps, 'distance' : value}
        self.children = [Reps(reps), Distance(value)]
        
 #   def __unicode__(self):
 #       return "<reps>" + self.xstr(self.reps) + "</reps>" + "<distance>" + self.xstr(self.distance) + "</distance>"

class Reps(Node):
    """
    Captures number of repetitions
    """
    def __init__(self, reps):
        self.type="reps"
        self.reps = reps
        self.data = reps
        
    def __unicode__(self):
        return self.xstr(self.reps)
        
class Distance(Node):
    """
    captures distance
    """
    def __init__(self, distance):
        self.type = "distance"
        self.distance = distance
        self.data = distance
    
    def __unicode__(self):
        return self.xstr(self.distance)
        
class Interval(Node):
    """
    Time length of a single rep in a set. Can be given in
    minutes:seconds (1:00) or in seconds (90s).
    """
    def __init__(self, minutes=0, seconds=0):
        self.type = "interval"
        self.minutes = minutes
        self.seconds = seconds
        self.data = self.minutes * 60 + self.seconds

    def total_seconds(self):
        return self.minutes * 60 + self.seconds
        
    def __unicode__(self):
        return self.xstr(self.total_seconds())

class Zone(Node):
    """
    Intensity level at which a rep is to be performed. Can be
    given in "EN#" or "Zone #" notation.

    Example::

        EN3

    """
    def __init__(self, zone=""):
        self.type="zone"
        self.zone = zone
        self.data = zone

    def __unicode__(self):
        self.xstr(self.zone) 

class Kick(Node):
    """
    Denotes set is a kick set.
    """
    def __init__(self, stroke="free"):
        self.type="kick"
        self.stroke = stroke
        self.data = stroke

    def __unicode__(self):
        return self.xstr(self.stroke)

class Drill(Node):
    """
    Denotes set is a drill set.
    """
    def __init__(self,stroke="",drill=""):
        self.type = "drill"
        self.stroke = stroke
        self.drill = drill
        self. data = drill

    def __unicode__(self):
        return 'drill'

class Stroke(Node):
    """
    Indicates stroke to be performed on a Set.

    (butter)fly, fr(eestyle), back(stroke), br(eaststroke) are the
    competetive strokes that may be indicated.
    """

    def __init__(self, stroke=""):
        self.type = "stroke"
        self.stroke = stroke
        self.data = stroke

    def __unicode__(self):
        return self.xstr(self.stroke)
