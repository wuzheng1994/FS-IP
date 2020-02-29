# -*-coding:utf-8-*-
from downuplink import *
import time
import os
import traceback

''''This code is designed for feature extraction.
Requirement: The original collected netowrk data constituted by the five-meta tuple.'''
if __name__ == "__main__":

    filenamelist = os.listdir(u"folder path")
    folder_path = u"folder path"
    print u'The number of files in current file folder is %d ' % len(filenamelist)
    Data = []
    start1 = time.time()
    for filename in filenamelist:
        uplink = []
        downlink = []
        datalink = []
        totallink = 0
# recommend the local ip
        local_ip = ''
        source_ip = []
        des_ip = []
        with open(folder_path+filename) as f:
            for line in f:
                source_ip.append(line.split()[1])
                des_ip.append(line.split()[2])
        total_ip = source_ip + des_ip
        s1 = list(set(total_ip))
        count_ip = [total_ip.count(i) for i in s1]
        r1 = sorted(count_ip)
        local_ip = s1[count_ip.index(r1[-1])]
        print 'local ip:',local_ip
        if raw_input("Approve of the local ip ? (Y/N)").upper() == 'Y':
            pass
        else:
            local_ip = raw_input('please input true local ip:').strip()


        with open(folder_path+filename) as f:
            for line in f:
                if not line: # appear null row
                    pass
                if line.split()[1] == local_ip:
                    uplink.append(line.split())
                if line.split()[2] == local_ip:
                    downlink.append(line.split())
                if line.split()[3] in ['HTTP','QUIC','UDP','TCP']:
                    datalink.append(line.split())
                totallink +=1
        try:
            # feature extraction
            start2 = time.time()
            f1 = downlink_avg_ps(downlink)
            f2 = uplink_avg_ps(uplink)
            f3 = downlink_max_ps(downlink)
            f4 = uplink_max_ps(uplink)
            f5 = downlink_valid_ip_ratio(downlink)
            f6 = uplink_ave_rate(uplink)
            f7 = downlink_ave_rate(downlink)
            f8 = uplink_var_ps(uplink)
            f9 = downlink_var_ps(downlink)
            f10= downlink_max_interval(downlink)
            f11= uplink_max_interval(uplink)
            f12= downlink_avg_interval(downlink)
            f13= uplink_avg_interval(uplink)
            f14= downlink_std_interval(downlink)
            f15= uplink_std_interval(uplink)
            f16= downlink_entropy_ps(downlink)
            f17= datalink_valid_ip_ratio(datalink,totallink)
            f18= downlink_uplink_rate_ratio(downlink, uplink)
            f19= downlink_up_counts_ratio(downlink,uplink)
            f20= downlink_up_bytes_ratio(downlink, uplink)
            f21= downlink_interval_pdf_entropy(downlink)
            f22= datalink_avg_ps(datalink)
            f23= datalink_avg_interval(datalink)
            f24= datalink_std_ps(datalink)
            f25= datalink_max_ps(datalink)
            f26= datalink_std_interval(datalink)
            f27= datalink_max_interval(datalink)
            f28= datalink_subflow_features(datalink)
            f29= downlink_cv_rate(downlink)
            f30= downlink_std_ps(downlink)
            f31= downlink_cv_interval(downlink)
            f32= uplink_cv_ps(uplink)
            f33= uplink_std_ps(uplink)
            f34= uplink_cv_interval(uplink)
            f35= uplink_std_interval(uplink)
            f36= datalink_cv_ps(datalink)
            f37= datalink_cv_interval(datalink)
            f38= datalink_cv_rate(datalink)
            f39= datalink_avg_rate(datalink)
            f40= datalink_std_rate(datalink)
        except ZeroDivisionError,e:
            print traceback.print_exc()
            sample = []
            Data.append(sample)
            print '%s take place error.' % i
            continue

        sample = []
        for j in range(1,41):
            exec 'sample.append(f%d),' % j
        Data.append(sample)
        comsumption = time.time() - start2
        print 'The %s  consumes %f s' % (filename,comsumption)
    print "The whole consumption is %f s" % eval(time.time())-eval(start1)
    print "The result is :"
    print Data