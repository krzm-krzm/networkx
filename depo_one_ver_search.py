import numpy as np
import pandas as pd
import networkx as nx
import math
from itertools import product
import matplotlib.pyplot as plt


def distance(x1, x2, y1, y2):
    d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return d


def Setting(FILENAME):
    mat = []
    with open('/home/kurozumi/デスクトップ/benchmark2/' + FILENAME, 'r', encoding='utf-8') as fin:
        for line in fin.readlines():
            row = []
            toks = line.split()
            for tok in toks:
                try:
                    num = float(tok)
                except ValueError:
                    continue
                row.append(num)
            mat.append(row)
    # インスタンスの複数の行（問題設定）を取り出す
    Setting_Info = mat.pop(0)  # 0:車両数、4:キャパシティ、8:一台あたりの最大移動時間(min)、9:一人あたりの最大移動時間(min)

    # デポの座標を取り出す
    depo_zahyo = np.zeros(2)  # デポ座標配列
    x = mat.pop(-1)
    depo_zahyo[0] = x[1]
    depo_zahyo[1] = x[2]

    request_number = len(mat) - 1

    # 各距離の計算
    c = np.zeros((len(mat), len(mat)), dtype=float, order='C')

    # eがtime_windowの始、lが終
    e = np.zeros(len(mat), dtype=int, order='C')
    l = np.zeros(len(mat), dtype=int, order='C')

    # テキストファイルからtime_windowを格納 & 各ノードの距離を計算し格納
    for i in range(len(mat)):
        e[i] = mat[i][5]
        l[i] = mat[i][6]
        for j in range(len(mat)):
            c[i][j] = distance(mat[i][1], mat[j][1], mat[i][2], mat[j][2])

    # 乗り降りの0-1情報を格納
    noriori = np.zeros(len(mat), dtype=int, order='C')
    for i in range(len(mat)):
        noriori[i] = mat[i][4]

    return Setting_Info, request_number, depo_zahyo, c, e, l, noriori

def setuzoku_node_list(dic): #移動できるノードの一覧辞書を返す関数、時間軸に関しては情報落ち
    node_dict = {}
    for id,info in dic.items():
        print(id,info.values())
        node_dict.setdefault(id[0],info.values())

    return  node_dict

"""
関数setuzoku_nodeについて
二個目のノードから再び(0,0)のノードが選ばれてしまうので何かしら分岐が必要
・ピックアップノードからデポに戻るの禁止
    ＊デポ以外の近いところを選択、どうしてもない場合、ドロップノードに行く
    
・6/20
    ＊ピックアップノードから関係ないドロップノードにいってしまう
    *
"""
def setuzoku_node_list2(dic,now_location,previous_location):
    min_weight=  float('inf')
    saitan_setuzoku_node = (0, 0)
    drop_kouho =(0.0)
    loop = 0
    if genzaichi==(0,0):
        for id, info in dic.items():
            print(id, info.values())
            if loop ==0:
                saitan_setuzoku_node=id
                min_weight = float(list(dic[saitan_setuzoku_node].values())[0])
            else:
                if float(list(dic[id].values())[0]) <min_weight:
                    saitan_setuzoku_node=id

            loop+=1
    elif noriori[now_location[0]] ==1:
        for id, info in dic.items():
            print(id, info.values())
            if id[0] == now_location[0] + Request:
                drop_kouho = id
            if loop == 0:
                if not id ==previous_location and not noriori[id[0]]==-1:
                    if check_node(G.adj[id], now_location) == 1:
                        saitan_setuzoku_node = id
                        min_weight = float(list(dic[saitan_setuzoku_node].values())[0])
            else:
                if not id == previous_location and not noriori[id[0]]==-1:
                    if float(list(dic[id].values())[0]) < min_weight:

                        if check_node(G.adj[id],now_location) ==1:
                            saitan_setuzoku_node = id
            loop += 1
        if saitan_setuzoku_node == (0,0):
            saitan_setuzoku_node = drop_kouho

    elif noriori[now_location[0]] ==-1:
        min_weight = float('inf')
        saitan_setuzoku_node = (0, 0)

        loop = 0
        for id, info in dic.items():
            print(id, info.values())
            if loop == 0:
                if not id ==previous_location:
                    if check_node(G.adj[id], now_location) == 1:
                        saitan_setuzoku_node = id
                        min_weight = float(list(dic[saitan_setuzoku_node].values())[0])
            else:
                if not id == previous_location:
                    if float(list(dic[id].values())[0]) < min_weight:
                        saitan_setuzoku_node = id
            loop += 1
    return saitan_setuzoku_node

"""
#別のピックアップノードを入れたあと、以前のピックアップをドロップできるか判定する
"""
def check_node(next_location_dic,now_location):
    flag =0
    for id,info in next_location_dic.items():
        if id[0] == now_location[0] + Request:
            flag =1
            break
    return flag


def saitan(dic):
    min_node =min(dic)
    min_weight= list(dic[min_node])[0]
    return  min_node,min_weight

def genzaich_update(tup):
    tup_new=list(tup)
    tup_new[1] = tup_new[1]+d
    return tuple(tup_new)
"""
関数network_updateについて
現在地のノードを削除したらいけません→この関数は使えないかも
一台分のルートが完成してから削除しましょう
"""
def network_update(network,removenode):
    for i in list(network.nodes()):
        if i[0] == removenode[0]:
            network.remove_node(i)

if __name__ == '__main__':
    FILENAME = 'darp01EX.txt'
    Setting_Info = Setting(FILENAME)
    Setting_Info_base = Setting_Info[0]

    Syaryo_max_time = Setting_Info_base[8]
    T = int(Setting_Info_base[5])  # 時間数
    n = int(Setting_Info[1]) + 1  # デポを含めた頂点数
    Request = int((n - 1) / 2)  # リクエスト数
    Distance = Setting_Info[3]  # 距離
    e = Setting_Info[4]  # early time
    l = Setting_Info[5]  # delay time
    d = 10  # 乗り降りにようする時間
    noriori = Setting_Info[6]

    Time_expand = 1

    G = nx.Graph()  # ノード作成
    for i in range(n):
        early_time = e[i]
        late_time = l[i]
        if e[i] == 0:
            early_time = 0
        add_node = range(early_time, late_time)
        if i == 0:
            G.add_node((0, 0))
        else:
            for j in add_node:
                if j % Time_expand == 0:
                    G.add_node((i, j))
    G.add_node((n, T + 1))
    # G.add_edge((0,0),(1,5),weight=Setting_Info[3][0][1])

    for a in range(n):
        early_time = e[a]
        late_time = l[a]

        add_node = range(early_time, late_time)
        for j in add_node:
            if j % Time_expand == 0:
                b = 0
                for i in range(n - 1):  # 各ノードからdepoに帰るエッジがつくられていない & ここのループだとdepoのノード同士がつながらないので改善が必要
                    if a == 0 and noriori[i + 1] > 0:
                        next_early_time = e[i + 1]
                        next_late_time = l[i + 1]

                        next_add_node = range(next_early_time, next_late_time)
                        for k in next_add_node:
                            if k % Time_expand == 0:
                                distance_check = math.ceil(Distance[a][i + 1])
                                if distance_check + j <= k:  # このedgeを追加するコードは無駄な処理を含んでいます。直す必要アリ(5/10)
                                    b = 1
                                    if a == i + 1:
                                        if k - j == 1:
                                            G.add_edge((0, 0), (i + 1, k), weight=Distance[a][i + 1])
                                    else:
                                        G.add_edge((0, 0), (i + 1, k), weight=Distance[a][i + 1])

                                if b == 1:
                                    break
                    elif not a == 0:
                        next_early_time = e[i + 1]
                        next_late_time = l[i + 1]

                        next_add_node = range(next_early_time, next_late_time)
                        for k in next_add_node:
                            if k % Time_expand == 0:
                                distance_check = math.ceil(Distance[a][i + 1])
                                if distance_check + j <= k:  # このedgeを追加するコードは無駄な処理を含んでいます。直す必要アリ(5/10)
                                    b = 1
                                    if a == i + 1:
                                        if k - j == 1:
                                            G.add_edge((a, j), (i + 1, k), weight=Distance[a][i + 1])
                                    else:
                                        G.add_edge((a, j), (i + 1, k), weight=Distance[a][i + 1])
                                if b == 1:
                                    b = 0
                                    break

    for i in range(n - 1):
        if noriori[i + 1] < 0:
            early_time = e[i + 1]
            late_time = l[i + 1]

            add_node = range(early_time, late_time)
            for j in add_node:
                if j % Time_expand == 0:
                    b = 0
                    depo_repeat = range(early_time, l[0])
                    for k in depo_repeat:
                        if k % Time_expand == 0:
                            distance_check = math.ceil(Distance[i + 1][0])
                            if j + distance_check <= k:
                                b = 1
                                G.add_edge((i + 1, j), (n, T + 1), weight=Distance[i + 1][0])
                            if b == 1:
                                break

    pos = {n: (n[1], -n[0]) for n in G.nodes()}  # ノードの座標に注意：X座標がノード番号、Y座標が時刻t
    # print(pos)
    # print(G.nodes())
    """
     loop = 0
    for i in range(T):
        G.add_edge((0, loop), (0, i + 1), weight=0)
        loop += 1
    e=5
    l=9
    L=list(range(e,l+1,1))
    for i in L:
        G.remove_node((4,i))
    nx.draw_networkx_nodes(G, pos, node_size=10, alpha=1, node_color='blue')
    nx.draw_networkx_edges(G, pos, width=1)
    plt.show()
    """
    print(FILENAME)
    print(Time_expand)
    print(nx.number_of_edges(G))
    print(nx.number_of_nodes(G))
    genzaichi = (0, 0)
    old_genzaichi = genzaichi
    print(G.adj[genzaichi])
    print(G.adj[genzaichi][(1,5)].values())
    print(G.adj[genzaichi].values())
    print(type(G.adj[genzaichi]))
    main_loop =0
    while True:
        setuzoku_Node=setuzoku_node_list2(G.adj[genzaichi],genzaichi,old_genzaichi)
        print(setuzoku_Node)



        genzaichi=setuzoku_Node

        '''
        nx.draw_networkx_nodes(G, pos, node_size=10, alpha=1, node_color='blue')
        nx.draw_networkx_edges(G, pos, width=1)
        plt.show()
        '''

        genzaichi = setuzoku_Node

        print(genzaichi)

        genzaichi = genzaich_update(genzaichi)
        print(genzaichi)
        main_loop+=1
        if main_loop ==3:
            break