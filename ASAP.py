from asyncio.windows_events import NULL
from cmath import nan
from msilib.schema import FileSFPCatalog
import xml.etree.ElementTree as ET

filename = 'graph2.xml'

class Node:
    id = 0  # ID
    type = "" # 演算子名
    time = -1 # スケジュール時間
    d = 0 # 実行時間
    m = 0 # mobility
    a = 0 # ラベル
    working = False

    def __init__(self, v):
        self.id = v.get("id")
        self.type = v.get("type")
        self.d = int(v.get("d"))

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
    tree = ET.parse(filename)
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
        S = []
        for v in node:
            prev_is_scheduled = True
            for e in edge:
                if e.next == node[v].id:    #ノードiの前のノードを探索                    
                    if node[e.prev].time == -1 or node[v].time != -1:     #もし前のノードがスケジュール済だったら
                        prev_is_scheduled = False
            if prev_is_scheduled:
                S.append(v)

        print(S)
        for i in S:
            
            max = 0
            prev_d = 0
            for e in edge:
                if e.next == node[i].id:
                    if max <= node[e.prev].time:
                        max = node[e.prev].time
                        prev_d = node[e.prev].d
            node[i].time = max + prev_d 
    for v in node:
        node[v].print()
    return node

def ALAP(node, edge, l):
    node['n'].time = l
    while node['0'].time == -1:   #node[o]がスケジュールされるまでループ
        for v in node:
            #print(v + "の時間") 
            #print(node[v].time)    
            NEXT_is_Scheduled = True       
            for e in edge:
                if e.prev == node[v].id:    #ノードiの後ろのノードを探索                    
                    if(node[e.next].time == -1):     #もし次のノードがスケジュールされてなかったら
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

'''def LIST(node, edge, a):
    l = 1
    node['0'].time = 0
    
    while node['n'].time == -1:
        for k in a:
            U = []
            T = []
            for v in node:
                PREV_is_Scheduled = True      
                for e in edge:
                    if e.next == node[v].id:    #ノードiの後ろのノードを探索                    
                        if node[e.prev].time == -1 or node[e.prev].time == l or node[e.prev].working:     #もし後ろのノードがスケジュールされてなかったら
                            PREV_is_Scheduled = False   #候補ではない                      
                if PREV_is_Scheduled and node[v].time == -1:             
                    if node[v].type == k:
                        U.append(v)
                    elif node[v].type == 'NOP':
                        U.append(v)
            for v in node:
                if node[v].working and node[v].type == k:
                    T.append(v)
            hoge = a[k] - len(T)
            print("U")
            print(U)
            print("T")
            print(T)
            for i in range(hoge):
                if len(U) > 0:
                    ham = U.pop(0)
                    node[str(ham)].time = l
                    if node[str(ham)].d > 1:
                        node[str(ham)].working = True
            for i in T:
                if node[str(i)].d == 1:
                    node[str(i)].working = False
                else:
                    node[str(i)].d -= 1

            

        l += 1
    for v in node:
        node[v].print()
    return node
'''

def LIST(node, edge, a):
    l = 1
    node['0'].time = 0
    while node['n'].time == -1:
        

        for k in a:
            U = []
            T = []
            S = []
            for v in node:   
                PREV_is_Scheduled = True      
                for e in edge:
                    if e.next == node[v].id:    #ノードiの後ろのノードを探索                    
                        if node[e.prev].time == -1 or node[e.prev].working:     #もし後ろのノードがスケジュールされてなかったら
                            PREV_is_Scheduled = False   #候補ではない                      
                if PREV_is_Scheduled and node[v].time == -1:             
                    if node[v].type == k or node[v].type == 'NOP':
                        U.append(v)
                
                if node[v].working and node[v].type == k:
                    T.append(v)

            hoge = a[k] - len(T)
            
            #print("U")
            #print(U)
            #print("T")
            #print(T)
            for i in range(hoge):
                if len(U) > 0:
                    S.append(U.pop(0))
            for i in S:
                node[i].time = l
                node[i].working = True

            #print("S")
            #print(S)
        
        for v in node:
            if node[v].working: 
                if node[v].d == 1:
                    node[v].working = False
                else:
                    node[v].d -= 1

        l += 1
    #for v in node:
    #    node[v].print()
    return node
def main():
    node_s, edge = init()
    node_l, edge = init()
    node , edge = init()
    node_list , edge = init()

    node_s = ASAP(node_s, edge)
    lambda_s = node_s['n'].time - node_s['0'].time
    print(node_s['n'].time)
    node_l = ALAP(node_l, edge, lambda_s)
    #node_l = ALAP(node_l, edge, 10)

    node = create_label(node, edge)
    #for v in node_l:
    #    node_l[v].print()
    


    a = {"M":3, "ALU":1}
    node_list = LIST(node_list, edge, a)
    #for v in node:
    #    node[v].print()
    
    
if __name__ == "__main__":
    main()

