# La Belle Balade

This project has been made under **24 Hours** for the **Facebook Paris Hack of 2019**  
This Hackathon was quite challenging: we didn't know each other before the event, we had very different profiles, etc. 
but with a "good" night of work, and the beautiful amenites of Facebook Paris, we managed to do something pretty great !

## The project

The aim of this project was to find a tourism itinerary given some constraints:
  * Limited time
  * Fixed departure point
  * Fixed destination point
  * User interests
  * Best points of interests should have the priority
    * Ranking is based on public opinion (Google Map, Trip advisor, etc.) **We did not have the time to finalize this**

We achieved a good result using:
  * [Mapbox](https://www.mapbox.com/) for the rendering of the map and the itinerary
  * [React](https://reactjs.org/) and [Webpack](https://webpack.js.org/) for the front dev
  * [Python](https://www.python.org/) for all the algorithms and back-end
  * [OpenStreetMap](https://www.openstreetmap.org) for fetching the points of interests

## How to launch it

You have to start **two** flask server, one to serve the front, the other to run the back-end API.  
The front listen on the port **8080**, the back on **5000**

```bash
# Launch the front
./front/server/app.py

# Launch the back
./server/app.py
```

## How it looks

![Gare de Lyon example](./example.png?raw=true)
_None of us is really good with web development nor a web designer, so we used [Webflow](https://webflow.com/)._
_Yes, for a page as simple as this, don't judge us please._

# The team

 - Song DUONG - [Github](https://github.com/lafius) - [LinkedIn](https://www.linkedin.com/in/song-duong-b73923175/)
 - Geoffrey CIDERON - [Github](https://github.com/geoffreycid) - [LinkedIn](https://www.linkedin.com/in/geoffrey-cideron/)
 - Pierre Liotet - [Github](https://github.com/robustepierre) - [LinkedIn](https://www.linkedin.com/in/pierre-liotet-a540989b/)
 - Louis VENTRE - [Github](https://github.com/Oxydros) - [LinkedIn](https://www.linkedin.com/in/louis-ventre-ba7708b6/)