
var React = require("react")
var createReactClass = require('create-react-class')

var API = require("../utils/api")

var ReactMapboxGl = require("react-mapbox-gl");
var MapFactory = ReactMapboxGl.Map;
var Layer = ReactMapboxGl.Layer;
var Feature = ReactMapboxGl.Feature;
var Source = ReactMapboxGl.Source
var Marker = ReactMapboxGl.Marker


module.exports = createReactClass({
    getInitialState(){
      return {
      }
    },
    _onClickMap(map, evt) {
      document.getElementById("lat").value = evt.lngLat.lat
      document.getElementById("long").value = evt.lngLat.lng
    },
    render() {
      const Map = MapFactory({
        accessToken: "INSERT_YOUR_OWN_MAPBOX_TOKEN",
        interactive: true
      });

      var remoteData = this.props.data || {}

      console.log(remoteData)

      if (!remoteData.coord) {
        return <Map
        center={[2.333333, 48.866667]}
        zoom={[12]}
        style="mapbox://styles/mapbox/streets-v9"
        containerStyle={{
          height: "100VH",
          width: "100%"
        }}
        onClick={this._onClickMap}
        />
      }

      var data = {
        type: "geojson",
        data: {
          type: "Feature",
          properties: {},
          geometry: remoteData.geometry
        }
      }

      var sw = {
        lon: remoteData.map_size[0],
        lat: remoteData.map_size[1]
      }

      var no = {
        lon: remoteData.map_size[2],
        lat: remoteData.map_size[3]
      }

      return <Map
      center={[2.333333, 48.866667]}
      zoom={[12]}
      style="mapbox://styles/mapbox/streets-v9"
      containerStyle={{
        height: "100VH",
        width: "100%"
      }}
      fitBounds={[[sw.lon, sw.lat], [no.lon, no.lat]]}
      onClick={this._onClickMap}
      >
        <Source id="source_id" geoJsonSource={data}/>
        <Layer
          type="line"
          sourceId="source_id"
        >
        </Layer>
        {
          remoteData && remoteData.coord.map((data, i) => {
           var lon = data[1];
           var lat = data[2];
           var iconMap = {
             museum: "museum-15",
             place_of_worship: "religious-christian-15",
             marketplace: "grocery-15",
             viewpoint: "attraction-15"
           }
           console.log(i)
           var icon;
           if (i == 0){
             icon = "castle-15"
           } else if (i == remoteData.coord.length - 1){
             icon = "embassy-15"
           } else {
             icon = iconMap[remoteData.places[i - 1]]
           }
            return <Layer
            type="symbol"
            layout={{
              "icon-image": icon,
              "icon-size": 2
              }}>
            <Feature
              coordinates={[lon, lat]}/>
          </Layer>
          })
        }
      </Map>;
    }
})
