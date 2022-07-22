from asyncio.windows_events import NULL
from cmath import nan
from msilib.schema import FileSFPCatalog
import xml.etree.ElementTree as ET
class Node:
    id = 0  # ID
    type = "" # 演算子名
    time = -1 # スケジュール時間
    d = 1 # 実行時間
    m = 0 # mobility
    a = 0 # ラベル

    def __init__(self, v):
        self.id = v.get("id")
        self.type = v.get("type")

    def print(self):
        print("id:" + self.id + ", type:" + self.type + ", time:" + str(self.time) + ",  label: " + str(self.a) + " d: " + str(self.d))

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
    node['0'].time = 0
    while node['n'].time == -1:   #ノードnがスケジュールされるまでループ
        for v in node:              
            for e in edge:
                if e.next == node[v].id:    #ノードiの前のノードを探索                    
                    if(node[e.prev].time != -1):     #もし前のノードがスケジュール済だったら
                        if node[v].time < node[e.prev].time + node[v].d:    #もし既存のノードのtimeより新しいノードのtimeが大きかったら
                            node[v].time = node[e.prev].time + node[v].d    #ノードのtimeを更新
    #for v in node:
        #node[v].print()
    return node

def ALAP(node, edge, l):
    node['n'].time = l
    while node['0'].time == -1:   #node[o]がスケジュールされるまでループ
        for v in node:    
            NEXT_is_Scheduled = True       
            for e in edge:
                if e.prev == node[v].id:    #ノードiの後ろのノードを探索                    
                    if(node[e.next].time == -1):     #もし後ろのノードがスケジュールされてなかったら
                        NEXT_is_Scheduled = False   #スケジュールしない                        
            if NEXT_is_Scheduled and node[v].time == -1:              
                min = 999
                for e in edge:
                    if node[v].id == e.prev:
                        if min > node[e.next].time:
                            min = node[e.next].time
                node[v].time = min - node[v].d

    for v in node:
        node[v].print()
    return node

def create_label(node, edge):
    node['n'].a = 1
    flag = 0
    while flag != len(node): 
        flag = 0
        for v in node:
            if node[v].a != 0:
                flag += 1
            for e in edge:
                if e.prev == node[v].id:
                    if(node[e.next].a != 0):
                        if node[v].a < node[e.next].a + 1:
                            node[v].a = node[e.next].a + 1
    for v in node:
        if node[v].type == "NOP":
            node[v].a = 0
        else:
            node[v].a -= 1
    return node

def Hu(node, edge, a):
    pass
def Max_label(node):
    max = 0
    for v in node:
        if max < node[v].a:
            max = node[v].a
    return max

def LIST(node, edge, a):
    l = 1
    flag =0
    for v in node:
        if node[v].type == "NOP":
            node[v].time = -1
        else:
            node[v].time = 0
    while flag < len(node):
        flag = 0

        for k in a:
            U = {}
            for v in node:              
                for e in edge:
                    if e.next == node[v].id:    #ノードiの前のノードを探索                    
                        if node[e.prev].time != 0:     #もし前のノードがスケジュール済だったら
                            U = {v:node[v]}
            for i in range(a[k]):
                for v in U:
                    print()
                


        l += 1        
        for v in node:
            if node[v] != 0:
                flag += 1

    return node

def main():
    node_s, edge = init()
    node_l, edge = init()
    node , edge = init()

    node_s = ASAP(node_s, edge)
    lambda_s = node_s['n'].time - node_s['0'].time
    node_l = ALAP(node_l, edge, lambda_s)
    #node_l = ALAP(node_l, edge, 6)
    node_l = create_label(node_l, edge)
    #for v in node_l:
    #    node_l[v].print()
    


    a = {"M":2, "ALU":2}
    node = LIST(node_l, edge, a)
    #for v in node:
    #    node[v].print()
    
    
if __name__ == "__main__":
    main()

