import geopandas as gp
import pandas as pd
from sklearn.cluster import KMeans

file_o = r'/Users/zhangqi/Documents/taxi/outputs/trip_o.shp'
file_d = r'/Users/zhangqi/Documents/taxi/outputs/trip_end.shp'
num_clusters = 100

trip_o = gp.GeoDataFrame.from_file(file_o, encoding = 'gb18030')
trip_o.head()
trip_end = gp.GeoDataFrame.from_file(file_d, encoding = 'gb18030')
trip_end.head()
trip_o['bz'] = 'O'
trip_end['bz'] = 'D'
trip_od = pd.concat([trip_o, trip_end], axis=0, join='outer', join_axes=None, ignore_index=False, keys=None,
                          levels=None, names=None)
#print(trip_od)
x = trip_od[['start_lon', 'start_lat']]
y_pred = KMeans(n_clusters=num_clusters, random_state=170).fit_predict(x)
df_out = pd.DataFrame({'trip_id':trip_od['trip_od'], 'bz':trip_od['bz'],
                       'lon': x['start_lon'], 'lat':x['start_lat'], 'tag': y_pred})
df_out.to_csv('../result/tag_point_' + str(num_clusters) + '.csv', index=False)
