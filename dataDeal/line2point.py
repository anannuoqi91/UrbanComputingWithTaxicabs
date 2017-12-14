"""
zhangqi

input [TRIP_ID,CALL_TYPE,ORIGIN_CALL,ORIGIN_STAND,TAXI_ID,TIMESTAMP,DAY_TYPE,MISSING_DATA,POLYLINE,TIME_SEQ]
      POLYLINE  "LINESTRING(-8.618643 41.141412,-8.618499 41.141376,-8.620326 ...)"
      TIME_SEQ  "[1372636858, 1372636873, 1372636888, 1372636903, 1372636918 ...]"

output all_points  所有GPS轨迹点['trip_id', 'day_type', 'isWeekday', 'lon', 'lat', 'timestamp', 'datetime', 'hour', 'seq']
       all_trip_o  所有轨迹起始点['trip_id', 'lon', 'lat']
       all_trip_d  所有轨迹终点['trip_id', 'lon', 'lat']
"""

import csv
from datetime import datetime,date,timedelta

def getData(input, out_all, out_o, out_d):
    with open(input) as fd:
        fd.readline()

        out1 = open(out_all, "a", newline="")
        csv_writer1 = csv.writer(out1, dialect="excel")
        row = ['trip_id', 'day_type', 'isWeekday', 'lon', 'lat', 'timestamp', 'datetime', 'hour', 'seq']
        csv_writer1.writerow(row)

        out2 = open(out_o, "a", newline="")
        csv_writer2 = csv.writer(out2, dialect="excel")
        row = ['trip_id', 'lon', 'lat']
        csv_writer2.writerow(row)

        out3 = open(out_d, "a", newline="")
        csv_writer3 = csv.writer(out3, dialect="excel")
        csv_writer3.writerow(row)

        for line in fd:
            splits = line.split('"')
            trip_id = splits[0].split(',')[0]
            day_type = splits[0].split(',')[6]
            point = splits[1].replace('LINESTRING(', '').replace(')', '')
            time = splits[3].replace('[', '').replace(']', '')
            tmp_point = point.split(',')
            tmp_time = time.split(',')

            csv_writer2.writerow([trip_id, float(tmp_point[0].split(' ')[0]), float(tmp_point[0].split(' ')[1])])
            csv_writer3.writerow([trip_id, float(tmp_point[-1].split(' ')[0]), float(tmp_point[-1].split(' ')[1])])

            seq = 1
            for i in range(len(tmp_point)):
                info = []
                info.append(str(trip_id))
                info.append(str(day_type))
                info.append(float(tmp_point[i].split(' ')[0]))
                info.append(float(tmp_point[i].split(' ')[1]))
                info.append(int(tmp_time[i]))
                dateArray = datetime.utcfromtimestamp(int(tmp_time[i]))
                otherStyleTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")
                otherStyleTime = otherStyleTime + timedelta(hours=-8)  #时区
                if (otherStyleTime.weekday() != 6) and (otherStyleTime.weekday() != 5):
                    info.append('weekday')
                else:
                    info.append('weekend')
                info.append(otherStyleTime)
                dt = dateArray.strftime("%H")
                info.append(dt)
                info.append(seq)
                csv_writer1.writerow(info)
                seq = seq + 1
        out1.close()
        out2.close()
        out3.close()
        print('ok')

filename = r'/Users/zhangqi/Documents/taxi/src_org/result/train_wkt.csv'
all_points = r'result/all_point_daytype.csv'
all_trip_o = r'../result/trip_o.csv'
all_trip_d = r'../result/trip_d.csv'

getData(filename, all_points, all_trip_o, all_trip_d)
