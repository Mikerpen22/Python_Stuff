n, m, k, j = [int(a) for a in input().split(',')]   # n個m維的點分成k群，以點j當成初始群中心

class Point:
    def __init__(self, index, args):
        self.coord = args
        self.index = index
        self.toCenters_min = float()

    def euclidean(self, center):
        dist_square = sum([(a-b)**2 for (a, b) in zip(self.coord, center.coord)])
        return dist_square

    def toEachCenter_min(self, round_q):

        # 只有第一輪要完整算過一遍，之後針對新center算
        if round_q == 0:
            self.toCenters_min = self.euclidean(centers[0])
        else:
            toCenter_i = self.euclidean(centers[-1])  # 算到最新的center距離
            if toCenter_i <= self.toCenters_min:
                self.toCenters_min = toCenter_i
        return self.toCenters_min


# 建立點list
p_lst = list()
for i in range(n):
    p_i = Point(i, [float(r) for r in input().split(',')])  # 座標跟是幾號點的資訊都打包成一個物件
    p_lst.append(p_i)

# 先把第一個點寫到centers
centers = [p_lst.pop(j-1)]

# 找幾個k-center就跑k-1次(第一個被選了)
for q in range(k-1):

    # 對每個點算他到各群中心距離中的最小值
    maxDists = [point.toEachCenter_min(q) for point in p_lst]

    # 各點到群中心的最小值之中，找出距離最大值的Index(距離相同比編號小)-->max會用最先碰到的最大值
    max_index = max(range(len(maxDists)), key=maxDists.__getitem__)

    centers.append(p_lst.pop(max_index))  # 記得pop掉存起來不然下一輪又算到同個點

print(*[ans_p.index+1 for ans_p in centers], sep=',')
