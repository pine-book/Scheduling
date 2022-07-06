import xml.etree.ElementTree as ET


class Graph:
    id = []
    type = []

    def set(v):
        Graph.id.append(v.get("id"))
        Graph.type.append(v.get("type"))
        
    def print():
        print(Graph.id)
        print(Graph.type)

tree = ET.parse('graph1.xml')

graph = Graph()

root = tree.getroot()
for v in root.findall("V"):
    Graph.set(v)
Graph.print()