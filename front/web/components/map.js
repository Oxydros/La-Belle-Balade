
var React = require("react")
var createReactClass = require('create-react-class')

var API = require("../utils/api")

var ReactMapboxGl = require("react-mapbox-gl").Map;
var Layer = ReactMapboxGl.Layer;
var Feature = ReactMapboxGl.Feature;


module.exports = createReactClass({
    getInitialState(){
      return {}
    },
    render() {
        const Map = ReactMapboxGl({
            accessToken: "pk.eyJ1IjoibGFmaXVzIiwiYSI6ImNqdHZpZnl2YTFybTAzeWxsbjJvNjY5eW4ifQ.wirxUDiWbhISy5PGNBHp1A",
            interactive: true,

          });

        return <Map
        center={[2.333333, 48.866667]}
        zoom={[12]}
        style="mapbox://styles/mapbox/streets-v9"
        containerStyle={{
          height: "100VH",
          width: "100%"
        }}>
      </Map>;
    }
})