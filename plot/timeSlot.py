import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def draw_speed_mean(data, outpng):
    # 按时间求均值
    grouped_mean = data.groupby('hour')['speed'].mean()
    grouped_mean = pd.DataFrame(grouped_mean)
    grouped_mean['hour'] = grouped_mean.index
    grouped_mean.columns = ['speed_avg', 'hour']
    # 均值
    speed_avg = speed['speed'].mean()
    # 绘图
    x = grouped_mean['hour']
    y = grouped_mean['speed_avg']
    plt.figure(figsize=(12, 6))
    plt.plot(x, y, linewidth=1.0)
    my_x_ticks = np.arange(0, 24, 1)
    plt.xticks(my_x_ticks)
    plt.hlines(speed_avg, 0, 23, linestyles='dashed')
    plt.xlabel('hour')
    plt.ylabel('speed')
    plt.title('speed_avg')
    plt.grid(True, linestyle="-.", color="r", linewidth="0.5")
    plt.savefig(outpng)
    #plt.show()

filename = '../result/all_speed_distance_daytype.csv'
speed = pd.read_csv(filename)
#weekday
weekday = speed[speed['daytype'] == 'weekday']
#weekend
weekend = speed[speed['daytype'] == 'weekend']

draw_speed_mean(speed, '../result/speed_all.png')
draw_speed_mean(weekday, '../result/speed_weekday.png')
draw_speed_mean(weekend, '../result/speed_weekend.png')


