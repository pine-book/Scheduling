from asyncio.windows_events import NULL
from cmath import nan
import xml.etree.ElementTree as ET
class Node:
    id = 0
    type = ""
    time = NULL
    d = 1
    m = 0
    a = 0

    def __init__(self, v):
        self.id = v.get("id")
        self.type = v.get("type")

    def print(self):
        print(self.id + " : " + self.type + " : " + str(self.time) + "  A : " + str(self.a))

class Edge:
    prev = ""
    next = ""

    def __init__(self, e):
        self.prev = e.get("prev")
        self.next = e.get("next")

    def print(self):
        print(self.prev + " ➡  " + self.next)

def init():
    tree = ET.parse('graph1.xml')
    root = tree.getroot()

    node = {}
    for v in root.findall("V"):
        node[v.get("id")] = Node(v)

    edge = []
    for e in root.findall("E"):
        edge.append(Edge(e))
    return node, edge

def ASAP(node, edge):
    node['0'].time = 1
    while node['n'].time == NULL:   #ノードnがスケジュールされるまでループ
        for v in node:              
            for e in edge:
                if e.next == node[v].id:    #ノードiの前のノードを探索                    
                    if(node[e.prev].time != 0):     #もし前のノードがスケジュール済だったら
                        if node[v].time < node[e.prev].time + node[v].d:    #もし既存のノードのtimeより新しいノードのtimeが大きかったら
                            node[v].time = node[e.prev].time + node[v].d    #ノードのtimeを更新

    #for v in node:
        #node[v].print()

    return node

def ALAP(node, edge, l):
    node['n'].time = l + 1
    while node['0'].time != 1:   #ノード0がスケジュールされるまでループ
        for v in node:            
            for e in edge:
                if e.prev == node[v].id:    #ノードiの後ろのノードを探索                    
                    if(node[e.next].time != 0):     #もし後ろのノードがスケジュール済だったら 
                        if node[v].time > node[e.next].time - node[v].d or node[v].time == 0:    #もし既存のノードのtimeより新しいノードのtimeが小さかったら
                            node[v].time = node[e.next].time - node[v].d    #ノードのtimeを更新

    #for v in node:
        #node[v].print()

    return node

def create_label(node, edge):
    node['n'].a = 1
    flag = 0
    while flag != len(node):   #ノード0がスケジュールされるまでループ
        flag = 0
        for v in node:
            if node[v].a != 0:
                flag += 1
            for e in edge:
                if e.prev == node[v].id:
                    if(node[e.next].a != 0):
                        if node[v].a < node[e.next].a + 1:
                            node[v].a = node[e.next].a + 1
    return node

def Hu(node, edge, a):
    pass

def main():
    node_s, edge = init()
    node_l, edge = init()
    node , edge = init()

    node_s = ASAP(node_s, edge)
    lambda_s = node_s['n'].time - node_s['0'].time - 1
    
    node_l = ALAP(node_l, edge, lambda_s)


    node_l = create_label(node_l, edge)
    for v in node_l:
        node_l[v].print()
    #print(lambda_s) 
    
if __name__ == "__main__":
    main()

