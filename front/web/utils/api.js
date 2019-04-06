var HTTP = require("./http")
var Qs = require('qs')

module.exports = {
    query_map: (research_settings) => {
        //Transform hh:mm into seconds
        var a = research_settings["time"].split(':')
        var time = (+a[0]) * 60 * 60 + (+a[1]) * 60 

        var data = {
            //Default start coordinate is Facebook Paris HQ
            lat_deb: 48.8695156,
            lon_deb: 2.3381157,
            lat_fin: research_settings["lat"] || "0",
            lon_fin: research_settings["long"] || "0",
            free_time: time,
            museum: research_settings["museum"] || "0",
            marketplace: research_settings["market"] || "0",
            viewpoint: research_settings["viewpoint"] || "0",
            place_of_worship: research_settings["religion"] || "0",
        }
        var qs = Qs.stringify(data)
        console.log(qs)
        return HTTP.get("http://localhost:5000/?" + qs)
    }
}