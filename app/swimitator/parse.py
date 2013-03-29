import json
import swim_parser
import swim_ast.traversal as traversal
from swim_ast.xml_visitor import SwimXmlVisitor, SwimXmlCloseVisitor
from swim_ast.json_visitor import SwimJsonVisitor, SwimJsonCloseVisitor

def get_xml(workout):
    p = swim_parser.parser
    res = p.parse(workout)
    sv = SwimXmlVisitor()
    cv = SwimXmlCloseVisitor()
    out = []
    traversal.xml_traverse(res, sv, cv, out)
    out.insert(0, '<?xml version="1.0" encoding="utf-8"?>')
    return '\n'.join(out)

def get_json(workout):
    p = swim_parser.parser
    res = p.parse(workout)
    sv = SwimJsonVisitor()
    cv = SwimJsonCloseVisitor()
    out = traversal.json_traverse(res, sv, cv, [])
    return json.dumps(json.loads(out), indent = 2)
