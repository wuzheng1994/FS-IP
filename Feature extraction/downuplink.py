# -*-coding:utf-8-*-
import os
import numpy as np
from math import log

'''Following functions are the feature extraction functions.
This is called by the file named run within the same folder.'''

def avg(s):
    avg = float(sum(s))/len(s)
    return avg
def std(s):
    if len(s) > 1:
        ave = avg(s)
        return (sum([(i-ave)**2  for i in s])/(len(s)-1))**0.5
    else:
        return 0

def skeness(s):
    ave = avg(s)
    st = std(s)
    return sum([(i-ave)**2  for i in s])^3 / st**3
def byte_rate(link):
    byte_rate = []
    for i in range(len(link)):
        inter = eval(link[i+1][0])-eval(link[i][0])
        if inter > 0: # prevent interval is equal and less than 0
            byte_rate.append(float(eval(link[i][-1])) / (inter*2**10))
        if i == (len(link) -2):
            break
    return byte_rate


# 1. average downlink packetsize (float)
def downlink_avg_ps(downlink):
    return avg([ eval(i[-1]) for i in downlink])
# 2. average uplink packetsize (float)
def uplink_avg_ps(uplink):
    return avg([ eval(i[-1]) for i in uplink])
# 3. max downlink packetsize (int)
def downlink_max_ps(downlink):
    return max([ eval(i[-1]) for i in downlink])
# 4. max uplink packetsize(int)
def uplink_max_ps(uplink):
    return max([ eval(i[-1]) for i in uplink])
# 5. avaliable valid number of ip (int)
def downlink_valid_ip_ratio(downlink,total):
    a = [i[-2] for i in downlink if i[-2] in ["TCP",'UDP','HTTP','QUIC']]
    return float(len(a))/total
# 6. average uplink rate (float)
def uplink_ave_rate(uplink):
    byterate = byte_rate(uplink)
    return avg(byterate)
# 7. average downlink rate (float)
def downlink_ave_rate(downlink):
    byterate = byte_rate(downlink)
    return avg(byterate)
# 8. std of uplink packetsize (float)
def uplink_var_ps(uplink):
    return std([eval(i[-1]) for i in uplink])
# 9. std of downlink packetsize (float)
def downlink_var_ps(downlink):
    return std([eval(i[-1]) for i in downlink])
# 10. max interval of downlink (float)
def downlink_max_interval(downlink):
    return max([eval(downlink[i][0]) - eval(downlink[i-1][0]) for i in range(1,len(downlink))])
# 11. max interval of uplink (float)
def uplink_max_interval(uplink):
    return max([eval(uplink[i][0]) - eval(uplink[i-1][0]) for i in range(1,len(uplink))])
# 12. average interval of downlink (float)
def downlink_avg_interval(downlink):
    return avg([eval(downlink[i][0]) - eval(downlink[i-1][0]) for i in range(1,len(downlink))])
# 13. average interval of uplink (float)
def uplink_avg_interval(uplink):
    return avg([eval(uplink[i][0]) - eval(uplink[i-1][0]) for i in range(1,len(uplink))])
# 14. std of interval of downlink (float)
def downlink_std_interval(downlink):
    return std([eval(downlink[i][0]) - eval(downlink[i-1][0]) for i in range(1,len(downlink))])
# 15. std of interval of uplink (float)
def uplink_std_interval(uplink):
    return std([eval(uplink[i][0]) - eval(uplink[i-1][0]) for i in range(1,len(uplink))])
# 16. entropy of downlink packetsize(only)(float)
def downlink_entropy_ps(downlink):
    packetsize = [eval(i[-1]) for i in downlink]
    set1 = set(packetsize)
    counts = [float(packetsize.count(i)) for i in set1]
    total = sum(counts)
    result = sum([-(i / total) * log(i / total, 2) for i in counts])
    return result
# 17. valid ip protocol number for datalink (only) (float)
def datalink_valid_ip_ratio(datalink,total):
    a = len(datalink)
    return float(a)/total
# 18. downlink_uplink_rate_ratio (float)
def downlink_uplink_rate_ratio(downlink, uplink):
    downlink = downlink_ave_rate(downlink)
    uplink = uplink_ave_rate(uplink)
    return float(downlink)/uplink
# 19. downlink_up_ps_ratio (float)
def downlink_up_counts_ratio(downlink,uplink):
    return float(len(downlink))/len(uplink)
# 20. downlink_up_bytes_ratio (float)
def downlink_up_bytes_ratio(downlink, uplink):
    downlink_byte = sum([eval(i[-1]) for i in downlink])
    uplink_byte = sum([eval(i[-1]) for i in uplink])
    result = float(downlink_byte) / uplink_byte
    return result
# 21. downlink_interval_pdf_entropy (float)
def downlink_interval_pdf_entropy(downlink):
    source_ip = [i[1] for i in downlink]
    num = [source_ip.count(i) for i in set(source_ip)]
    total = sum(num)
    return sum([-(float(i) / total) * log(float(i) / total, 2) for i in num])
# 22. average packetsize of datalink (float)
def datalink_avg_ps(datalink):
    # print datalink
    try:
        ave = avg([eval(i[-1]) for i in datalink])
    except NameError,e:
        pass
    return ave
# 23. average interval of datalink
def datalink_avg_interval(datalink):
    return avg([eval(datalink[i][0]) - eval(datalink[i-1][0]) for i in range(1,len(datalink))])
# 24. std of packetsize of datalink
def datalink_std_ps(datalink):
    st = std([eval(i[-1]) for i in datalink])
    return st
# 25. maximum packetsize of datalink(int)
def datalink_max_ps(datalink):
    return max([eval(i[-1]) for i in datalink])
# 26. std interval of datalink(float)
def datalink_std_interval(datalink):
    return std([eval(datalink[i][0]) - eval(datalink[i-1][0]) for i in range(1,len(datalink))])
# 27. maximun interval of datalink
def datalink_max_interval(datalink):
    return max([eval(datalink[i][0]) - eval(datalink[i-1][0]) for i in range(1,len(datalink))])
# 28. output subflow aware features including number of subflows, average packets of subflow, entropy number of subflows std packets of subflows  average packetsize of subflow
def datalink_subflow_features(datalink):
    info = [(i[1], i[2],eval(i[-1])) for i in datalink]
    counts = []
    sf_ps = []
    last_ip = ''
    count = 0
    pscount = 0
    for i in range(len(info)):
        if last_ip == info[i][0]:
            count +=1
            pscount+= info[i][-1]
        else:
            if count > 1:
                counts.append(count)
                sf_ps.append(pscount)
            count = 1
            pscount = info[i][-1]
            last_ip = info[i][0]
        if i == (len(info) - 1) and count > 1:
            counts.append(count)
            sf_ps.append(pscount)

    # print counts
    total = sum(counts)
    avg_counts = avg(counts)
    entropy_counts = sum([-(float(i) / total) * log(float(i) / total, 2) for i in counts])
    std_counts = std(counts)
    avg_byte = avg(sf_ps)
    return (len(counts),avg_counts,entropy_counts,std_counts,avg_byte)

# 29. coefficient variation of downlink rate (float)
def downlink_cv_rate(downlink):
    a = downlink_avg_ps(downlink)
    s = downlink_std_ps(downlink)
    return s/a
# 30. downlink packetsize std (float)
def downlink_std_ps(downlink):
    return std([eval(i[-1]) for i in downlink])
# 31. coefficient variation of downlink rate(float)
def downlink_cv_interval(downlink):
    a = downlink_avg_interval(downlink)
    s = downlink_std_interval(downlink)
    return s/a
# 32. coefficient variation of uplink rate (float)
def uplink_cv_ps(uplink):
    a = uplink_avg_ps(uplink)
    s = uplink_std_ps(uplink)
    return s/a
# 33. uplink packetsize std (float)
def uplink_std_ps(uplink):
    return std([eval(i[-1]) for i in uplink])
# 34. coefficient variation of uplink interval (float)
def uplink_cv_interval(uplink):
    a = uplink_avg_interval(uplink)
    s = uplink_std_interval(uplink)
    return s/a
# 35. uplink_std_interval(float)
def uplink_std_interval(uplink):
    return std([eval(uplink[i][0]) - eval(uplink[i - 1][0]) for i in range(1, len(uplink)) if eval(uplink[i][0]) - eval(uplink[i - 1][0])>0])
# 36. datalink_cv_ps
def datalink_cv_ps(datalink):
    a = datalink_avg_ps(datalink)
    s = datalink_std_ps(datalink)
    return s/a
# 37. coefficient variation of datalink rate (float)
def datalink_cv_rate(datalink):
    a = datalink_avg_rate(datalink)
    s = datalink_std_rate(datalink)
    return s/a
# 38. coefficient variation of datalink interval (float)
def datalink_cv_interval(datalink):
    a = datalink_avg_interval(datalink)
    s = datalink_std_interval(datalink)
    return s/a
# 39. average datalink rate
def datalink_avg_rate(datalink):
    byterate = byte_rate(datalink)
    return avg(byterate)
# 40. std datalink rate
def datalink_std_rate(datalink):
    byterate = byte_rate(datalink)
    return std(byterate)

