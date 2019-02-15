import time

start_time = time.time()

n, m, k, j = [int(a) for a in input().split(',')]  # n個m維的點分成k群，以點j當成初始群中心


class Point:
    def __init__(self, index, args, isCenter=False):
        self.index = index
        self.coord = args
        self.isCenter = isCenter

    def euclidean(self, center):
        dist_square = sum([(a - b) ** 2 for (a, b) in zip(self.coord, center.coord)])
        return dist_square

    def toEachCenter_min(self):
        if self.isCenter is False:
            return min(map(lambda x: self.euclidean(x), [p for p in p_lst if p.isCenter == True]))
        else:
            return 0

# 建立點list
p_lst = list()
for i in range(n):
    p_i = Point(i, [float(r) for r in input().split(',')], False)  # 座標跟是幾號點的資訊都打包成一個物件
    p_lst.append(p_i)

# 找幾個k-center就跑k-1次(第一個被選了)
cur_cen = p_lst[j-1]  # j-1才是index
cur_cen.isCenter = True

for q in range(k - 1):

    # 對每個點算他到各群中心距離中的最小值
    maxDists = [point.toEachCenter_min() for point in p_lst]

    # 各點到群中心的最小值之中，找出距離最大值(距離相同比編號小)-->max會用最先碰到的最大值
    max_dist = max(maxDists)
    cur_cen = p_lst[maxDists.index(max_dist)]
    cur_cen.isCenter = True


print(*[p.index+1 for p in reversed(p_lst) if p.isCenter == True], sep=',')

print("--- %s seconds ---" % (time.time() - start_time))
