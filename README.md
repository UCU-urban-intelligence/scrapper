Command to run API: <br/>
```$ docker-compose up```


routes: <br/>

* localhost:8000/processing POST <br/>
```json
{
    "id": "Kyiv1",
    "bbox": [-79.486170,43.694577,-79.458413,43.713523]
}
```
   <br />
NOTE: <br/>
BBOX format EPSG 4326 [Lower Left (west, south) Upper Right (east, north)] <br />

Like [-66.577148,-30.278044,-50.756836,-22.034730]

## OSM data

Command to get geometry data from OSM using bbox:

`$ python scripts/buildings.py <lat1> <lng1> <lat2> <lng2>`

E. g. (Kyiv buildings):

`$ python scripts/buildings.py 50.303376 30.217896 50.602416 30.841370`

Output will be located in `out.geojson`

### P.S.
If you have some problems with installing dependencies try to call `sudo apt-get install python-dev`.
For more info check look [here](https://github.com/MeetMe/newrelic-plugin-agent/issues/151)