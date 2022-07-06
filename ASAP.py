import xml.etree.ElementTree as ET
class Node:
    id = 0
    type = ""

    def __init__(self, v):
        self.id = v.get("id")
        self.type = v.get("type")

    def print(self):
        print(self.id + ":" + self.type)

class Edge:
    prev = ""
    next = ""

    def __init__(self, e):
        self.prev = e.get("prev")
        self.next = e.get("next")

    def print(self):
        print(self.prev + ":" + self.next)

tree = ET.parse('graph1.xml')

root = tree.getroot()

node = []
for v in root.findall("V"):
    node.append(Node(v))
for i in range(len(node)):
    node[i].print()

edge = []
for e in root.findall("E"):
    edge.append(Edge(e))
for i in range(len(edge)):
    edge[i].print()

