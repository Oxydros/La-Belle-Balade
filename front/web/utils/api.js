var HTTP = require("./http")
var Qs = require('qs')

module.exports = {
    query_map: (research_settings) => {
        //Transform hh:mm into seconds
        var a = research_settings["time"].split(':')
        var time = (+a[0]) * 60 * 60 + (+a[1]) * 60 

        var data = {
            lat_deb: 48.8695156,
            lon_deb: 2.3381157,
            lat_fin: research_settings["lat"] || "0",
            lon_fin: research_settings["long"] || "0",
            free_time: time,
            museum: research_settings["museum"] || "0",
            market: research_settings["market"] || "0",
            parc: research_settings["parc"] || "0",
            religion: research_settings["religion"] || "0",
            art: research_settings["art"] || "0",
        }
        var qs = Qs.stringify(data)
        console.log(qs)
        return HTTP.get("http://localhost:5000/?" + qs)
    }
}