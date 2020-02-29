# encoding: utf-8
from matplotlib import pyplot as plt
from pylab import *
from collections import Counter

'''This code is designed for ploting the communication graph.
Requirement: The original collected netowrk data constituted by the five-meta tuple.'''

mpl.rcParams['font.sans-serif'] = ['Times New Roman']
mpl.rcParams['savefig.dpi'] = 600 #图片像素
mpl.rcParams['figure.dpi'] = 600 #分辨率
matplotlib.rcParams.update({'font.size': 20})

import time
start = time.time()
'''读文件'''
uplink = []
downlink = []
datalink = []
protocol = ['UDP', 'TCP']

f = r'file_path'

local_ip = 'Ip of the host machine'
with open(f) as f1:
    totallink = 0
    for line in f1:
        if not line:  # appear null row
            pass
        totallink += 1
        try:
            if line.split()[3] in protocol:
                datalink.append(line.split())
            elif not isinstance(line.split()[-1], str):
                protocol.append(line.split()[3])
                datalink.append(line.split())
        except IndexError as e:
            print line, e
    for l in datalink:
        if l[1] == local_ip:
            uplink.append(l)
        if l[2] == local_ip:
            downlink.append(l)

'''统计源地址及目的地址'''
pro = Counter(protocol)
des_ip = local_ip

src_ip = Counter([i[1] for i in downlink[:20000]])

cat = 'category'
src_ip_y = [[1,float((i+1))/(len(src_ip)+1)] for i in range(len(src_ip)+1)]
src_ip_coor = dict(zip(src_ip,src_ip_y))

print src_ip_coor

des_ip_coor = {des_ip:[0,0.5]}
pro_ip_y = [[2,float((i+1))/(len(protocol)+1)] for i in range(len(protocol)+1)]
pro_coor = dict(zip(protocol,pro_ip_y))
category = {cat:[3,0.5]}

print category

linewidth = 0.5

'''画图'''
fig,axs = plt.subplots()
x = range(4)
for i in range(4):
    plt.axvline(x=x[i],linewidth=1, color='r')
for i in src_ip_coor:
    plt.text(src_ip_coor[i][0]+0.1,src_ip_coor[i][1],i,fontsize=3)
    plt.scatter(src_ip_coor[i][0],src_ip_coor[i][1],marker=1)
for i in des_ip_coor:
    plt.text(des_ip_coor[i][0]+0.1,des_ip_coor[i][1],i)
    plt.scatter(des_ip_coor[i][0], des_ip_coor[i][1], marker=1)
for i in pro_coor:
    plt.text(pro_coor[i][0]+0.1,pro_coor[i][1],i,fontsize=15)
    plt.scatter(pro_coor[i][0],pro_coor[i][1], marker=1)
for i in category:
    plt.text(category[i][0]+0.1,category[i][1],i,fontsize=25,rotation=90)
    plt.scatter(category[i][0],category[i][1], marker=1)
for i in range(len(downlink[:20000])):
    temp = downlink[i]
    src = temp[1]
    des = temp[2]
    proto = temp[3]
    # print src, des, proto
    plot([src_ip_coor[src][0],des_ip_coor[des][0]],[src_ip_coor[src][1],des_ip_coor[des][1]],c='black',linewidth=linewidth)
    plot([src_ip_coor[src][0],pro_coor[proto][0]],[src_ip_coor[src][1],pro_coor[proto][1]],c='black',linewidth=linewidth)
for i in pro_coor:
    plot([pro_coor[i][0],category[cat][0]],[pro_coor[i][1],category[cat][1]],c='black',linewidth=linewidth)
plt.ylim([0,1])
# plt.xlim([-0.5,3.5])
plt.xticks(range(4),['desIP','srcIP','protocol','category'],fontsize=25)
ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['left'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['bottom'].set_color('none')
ax.set_yticks([])
plt.tight_layout()
plt.savefig('output path',dpi=400)

plt.show()

end = time.time()
elaps = end-start
print elaps


