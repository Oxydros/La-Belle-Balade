
var React = require("react")
var createReactClass = require('create-react-class')

var API = require("../utils/api")

var ReactMapboxGl = require("react-mapbox-gl");
var MapFactory = ReactMapboxGl.Map;
var Layer = ReactMapboxGl.Layer;
var Feature = ReactMapboxGl.Feature;
var Source = ReactMapboxGl.Source


module.exports = createReactClass({
    getInitialState(){
      return {}
    },
    render() {
        const Map = MapFactory({
            accessToken: "pk.eyJ1IjoibGFmaXVzIiwiYSI6ImNqdHZpZnl2YTFybTAzeWxsbjJvNjY5eW4ifQ.wirxUDiWbhISy5PGNBHp1A",
            interactive: true,

          });

        var data = {
          type: "geojson",
          data: {
            type: "Feature",
            properties: {},
            geometry: this.props.geometry
          }
        }

        console.log(data)

        return <Map
        center={[2.333333, 48.866667]}
        zoom={[12]}
        style="mapbox://styles/mapbox/streets-v9"
        containerStyle={{
          height: "100VH",
          width: "100%"
        }}>
        <Source id="source_id" geoJsonSource={data}/>
        <Layer
          type="line"
          sourceId="source_id"
        >
        </Layer>
      </Map>;
    }
})