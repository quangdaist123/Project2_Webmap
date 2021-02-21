import folium
import pandas as pd


def produce_icon(ele):
    icon = 'fire'
    return folium.Icon(color=color(ele), icon=icon)

def color(ele):
    if ele < 1000:
        return 'green'
    elif ele < 2000:
        return 'orange'
    else:
        return 'red'


data = pd.read_csv('./data/Volcanoes.txt.txt')
locations = list(zip(data['LAT'], data['LON']))
elevations = list(data['ELEV'])

my_map = folium.Map(location=[data['LAT'].mean(), data['LON'].mean()], zoom_start=5, control_scale=True)

ft_group_1 = folium.FeatureGroup(name='Volcanoes')
for loc, ele in zip(locations, elevations):
    marker = folium.CircleMarker(location=loc, popup=str(ele)+' m', stroke=True, radius=7,
                                 opacity=0.4, color='#782E1E', fill_color=color(ele), fill=True, fill_opacity=0.5)
    ft_group_1.add_child(marker)

ft_group_2 = folium.FeatureGroup(name='Choropleth')
json = open('./data/usa.json', 'r', encoding='utf-8-sig').read()
geojson_data = folium.GeoJson(data=json)
ft_group_2.add_child(geojson_data)

# Save the map
my_map.add_child(ft_group_1)
my_map.add_child(ft_group_2)
my_map.add_child(folium.LayerControl())
my_map.save("./data/USA_map.html")