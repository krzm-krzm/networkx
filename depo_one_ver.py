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
    with open('/home/kurozumi/デスクトップ/benchmark/' + FILENAME, 'r', encoding='utf-8') as fin:
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


if __name__ == '__main__':
    FILENAME = 'darp01_ex.txt'
    Setting_Info = Setting(FILENAME)
    Setting_Info_base = Setting_Info[0]

    T = int(Setting_Info_base[5])  # 時間数
    n = int(Setting_Info[1]) + 1  # デポを含めた頂点数
    Request = int((n - 1) / 2)  # リクエスト数
    Distance = Setting_Info[3]  # 距離
    e = Setting_Info[4]  # early time
    l = Setting_Info[5]  # delay time

    noriori = Setting_Info[6]

    G = nx.Graph()  # ノード作成
    for i in range(n):
        early_time = e[i] + 1
        late_time = l[i] + 1
        if e[i] == 0:
            early_time = 0
        add_node = range(early_time, late_time)
        if i == 0:
            G.add_node((0,0))
        else:
            for j in add_node:
                G.add_node((i, j))
    G.add_node((i+1,T+1))
    # G.add_edge((0,0),(1,5),weight=Setting_Info[3][0][1])

    
    
    for a in range(n):
        early_time = e[a] + 1
        late_time = l[a] + 1
        if e[a] == 0:
            early_time = 0

        add_node = range(early_time, late_time)
        if a==0:
            for i in range(n - 1):  # 各ノードからdepoに帰るエッジがつくられていない
                if noriori[i+1] >0:
                    next_early_time = e[i + 1] + 1
                    next_late_time = l[i + 1] + 1
                    if e[i + 1] == 0:
                        next_early_time = 0
                    next_add_node = range(next_early_time, next_late_time)
                    for k in next_add_node:
                        distance_check = math.ceil(Distance[a][i + 1])
                        if distance_check  <= k:  # このedgeを追加するコードは無駄な処理を含んでいます。直す必要アリ(5/10)
                                G.add_edge((0, 0), (i + 1, k), weight=Distance[a][i + 1])
        else:
            for j in add_node:
                for i in range(n - 1):  # 各ノードからdepoに帰るエッジがつくられていない
                    next_early_time = e[i + 1] + 1
                    next_late_time = l[i + 1] + 1
                    if e[i + 1] == 0:
                        next_early_time = 0
                    next_add_node = range(next_early_time, next_late_time)
                    for k in next_add_node:
                        distance_check = math.ceil(Distance[a][i + 1])
                        if distance_check + j <= k:  # このedgeを追加するコードは無駄な処理を含んでいます。直す必要アリ(5/10)
                            if a == i + 1:
                                if k - j == 1:
                                    G.add_edge((a, j), (i + 1, k), weight=Distance[a][i + 1])
                            else:
                                G.add_edge((a, j), (i + 1, k), weight=Distance[a][i + 1])


    for i in range(n - 1):
        if noriori[i+1] <0:
            early_time = e[i + 1] + 1
            late_time = l[i + 1] + 1
            if e[i + 1] == 0:
                early_time = 0
            add_node = range(early_time, late_time)
            for j in add_node:
                if j + distance_check <= T+1:
                    G.add_edge((i + 1, j), (n, T+1), weight=Distance[i + 1][0])

    pos = {n: (n[1], -n[0]) for n in G.nodes()}  # ノードの座標に注意：X座標がノード番号、Y座標が時刻t
    # print(pos)
    # print(G.nodes())

    """
    e=5
    l=9
    L=list(range(e,l+1,1))
    for i in L:
        G.remove_node((4,i))
    nx.draw_networkx_nodes(G, pos, node_size=10, alpha=1, node_color='blue')
    nx.draw_networkx_edges(G, pos, width=1)
nx.draw_networkx_nodes(G, pos, node_size=10, alpha=1, node_color='blue')
    nx.draw_networkx_edges(G, pos, width=1)
    plt.show()
    plt.show()
    """

    #print(G.edges())
    print(nx.number_of_edges(G))
    print(nx.number_of_nodes(G))


