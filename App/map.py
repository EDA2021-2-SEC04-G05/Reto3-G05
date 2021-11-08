from flask import Flask
import folium

app = Flask(__name__)


@app.route('/')
def index():
    start_coords = (34.165,-106.025)
    folium_map = folium.Map(location=start_coords,
                            tiles="Stamen Terrain",
                            min_lot=-109.05,
                            max_lot=-103.00,
                            min_lat=31.33,
                            max_lat=37.00,
                            max_bounds=True,
                            zoom_start = 9,
                            #max_zoom = 5,
                            #min_zoom =4,
                            width = '100%',
                            height = '100%') 
                            #zoom_control=False)

    """
    tooltip = "Click me!"

    folium.Marker(
    [45.3288, -121.6625], popup="<i>Mt. Hood Meadows</i>", tooltip=tooltip
    ).add_to(folium_map)
    folium.Marker(
    [45.3311, -121.7113], popup="<b>Timberline Lodge</b>", tooltip=tooltip
    ).add_to(folium_map)
    """
    return folium_map._repr_html_()


if __name__ == '__main__':
    app.run(debug=True)
