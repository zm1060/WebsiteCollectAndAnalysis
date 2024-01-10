import folium
import json

geo_data = 'china.json'

# Explicitly specify the encoding (utf-8)
with open(geo_data, 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)

map = folium.Map(location=[35.871669, 104.101399], zoom_start=5)

folium.Choropleth(
    geo_data=geojson_data,
    name='China',
    data=None,  # You can provide data for coloring if needed
    columns=None,
    key_on='feature.id',  # This assumes that the GeoJSON features have unique IDs
    fill_color='orange',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='China Boundaries'
).add_to(map)

map.save('china.html')
map
