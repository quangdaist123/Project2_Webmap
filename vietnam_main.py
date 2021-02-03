import json
import pandas as pd
import folium.plugins
import utils

dataset = pd.read_csv('./data/vn.csv',  encoding='utf-8-sig')
with open('./data/vn.json', 'r', encoding='utf-8-sig') as f:
    geo_data = json.loads(f.read())


my_map = folium.Map(location=[dataset['lat'].mean(), dataset['lng'].mean()],
                    tiles='OpenStreetMap',
                    zoom_start=7,
                    min_zoom=7,
                    max_zoom=12)

locations = list(zip(dataset['lat'], dataset['lng']))
city_name = dataset['city']
admin_city_name = dataset['admin_name']

# Towns/Cites layer
ft_group_1 = folium.FeatureGroup(name='Cites')
# Create cluster by province
for province in geo_data['features']:
    cluster = folium.plugins.MarkerCluster(options={'showCoverageOnHover': False,
                                                    'zoomToBoundsOnClick': True,
                                                    'spiderfyOnMaxZoom': False,
                                                    'disableClusteringAtZoom': 11})
    for loc, city, ad_city in zip(locations, city_name, admin_city_name):
        marker = folium.Marker(location=loc,
                               tooltip=f'<strong>{city}</strong>',
                               icon=folium.features.CustomIcon('./data/map-marker.png', icon_size=(20, 20)))
        # Add marker according to provinces
        if ad_city == province['properties']['name']:
            marker.add_to(cluster)

    ft_group_1.add_child(cluster)

density_dataset = pd.read_csv('./data/mat-do-dan-so-vn.csv')
path = './data/vn.json'
utils.correct_data(density_dataset, path)

# Population density layer
ft_group_2 = folium.Choropleth(geo_data=geo_data,
                               data=density_dataset,
                               columns=['admin_name', 'density'],
                               key_on='feature.properties.name',
                               fill_color='YlOrRd',
                               fill_opacity=0.6,
                               line_opacity=0.8,
                               legend_name='Mật độ dân số (người/km2)',
                               name='Mật độ dân số'
                               )

my_map.add_child(ft_group_1)
my_map.add_child(ft_group_2)
my_map.add_child(folium.LayerControl())
my_map.save('./data/VN_map.html')
