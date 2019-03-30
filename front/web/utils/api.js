var HTTP = require("./http")
var Qs = require('qs')

module.exports = {
    query_map: (interest, lat, long, hstart, hend) => {
        var data = {
            interest: interest || "museum",
            lat_deb: 48.8695156,
            lon_deb: 2.3381157,
            lat_fin: lat || "0",
            lon_fin: long || "0",
            hstart: hstart || "12:00",
            hend: hend || "14:00"
        }
        console.log("Making post request with ")
        console.log(data)
        var qs = Qs.stringify(data)
        console.log(qs)
        return HTTP.get("http://localhost:5000/?" + qs)
    }
}