"""
zhangqi

input ['trip_id', 'day_type', 'isWeekday', 'lon', 'lat', 'timestamp', 'datetime', 'hour', 'seq']

output all_speed_distance  所有GPS轨迹点的速度和距离
                           ['trip_id', 'day_type', 'isWeekday', 'lon', 'lat', 'datetime', 'hour', 'seq', 
                           'speed', 'distance']
"""

from math import radians, cos, sin, asin, sqrt
from datetime import datetime,timedelta
import pandas as pd
import csv

def haversine(lon1, lat1, lon2, lat2):  # 经度1，纬度1，经度2，纬度2 （十进制度数）
    """ 
    Calculate the great circle distance between two points  
    on the earth (specified in decimal degrees) 
    """
    """
    lon1 = point1[0]
    lat1 = point1[1]
    lon2 = point2[0]
    lat2 = point2[1]
    """
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为公里
    return c * r * 1000


def caculate(input, output):
    point = pd.read_csv(input)
    point.sort_values(by=['trip_id', 'seq'], axis=0, ascending=True)
    out = open(output, "a", newline="")
    csv_writer = csv.writer(out, dialect="excel")
    row = ['trip_id', 'day_type', 'isWeekday', 'day', 'hour', 'speed', 'distance']
    csv_writer.writerow(row)
    for i in range(len(point)):
        info = []
        if point.iat[i, 0] == point.iat[i + 1, 0]:
            info = []
            lon1 = point.iat[i, 3]
            lat1 = point.iat[i, 4]
            lon2 = point.iat[i + 1, 3]
            lat2 = point.iat[i + 1, 4]
            #i和i+1
            distance = haversine(lon1, lat1, lon2, lat2)  #m
            speed = distance / 15 * 3.6  # km/h
            info.append(point.iat[i, 0])
            info.append(point.iat[i, 1])
            info.append(point.iat[i, 2])
            info.append(point.iat[i, 3])
            info.append(point.iat[i, 4])
            info.append(point.iat[i, 6])
            info.append(point.iat[i, 7])
            info.append(point.iat[i, 8])
            info.append(speed)
            info.append(distance)
            csv_writer.writerow(info)
    out.close()

filename = r'../result/all_speed_daytype.csv'
all_speed_distance = r'../result/all_speed_distance_daytype.csv'