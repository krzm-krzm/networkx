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
            toks = line.split(' ')
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
    e = np.zeros(len(mat), dtype=float, order='C')
    l = np.zeros(len(mat), dtype=float, order='C')

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

if __name__ =='__main__':
    FILENAME = 'darp01.txt'
    Setting_Info =Setting(FILENAME)
    Setting_Info_base =Setting_Info[0]

    #T = Setting_Info_base[5]    #時間数
    T = 3
    n= int(Setting_Info[1])+1 #デポを含めた頂点数
    Request = int((n-1)/2)  #リクエスト数
    Distance = Setting_Info[3]  #距離
    e = Setting_Info[4] #early time
    l=Setting_Info[5]   #delay time

    N=10

    G = nx.Graph()
    for i in range(N):
        for j in range(T):
            G.add_node((i,j))

    pos = {n: (n[0], -n[1]) for n in G.nodes()}
    print(pos)
    print(G.nodes())

    G.remove_node((0,0))
    nx.draw_networkx_nodes(G, pos, node_size=30, alpha=1, node_color='blue')

    plt.show()

