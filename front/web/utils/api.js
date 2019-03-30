var HTTP = require("./http")

module.exports = {
    query_map: (interest, lat, long, hstart, hend) => {
        var data = {
            interest: interest || "museum",
            lat: lat || "0",
            long: long || "0",
            hstart: hstart || "12:00",
            hend: hend || "14:00"
        }
        return HTTP.post("http://localhost:5000/query", data)
    }
}