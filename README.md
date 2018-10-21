Command to run API: <br/>
```$ docker-compose up```


routes: <br/>

* localhost:8000/processing POST <br/>
```json
  {
    "bbox": []
  }
```
   <br />
NOTE: <br/>
BBOX format EPSG 4326 [Lower Left (west, south) Upper Right (east, north)] <br />

Like [-66.577148,-30.278044,-50.756836,-22.034730]

## OSM data

Comand to get geometry data from OSM using bbox:

`$ python scripts/buildings.py <lat1> <lng1> <lat2> <lng2>`

E. g. (Kyiv buildings):

`$ python scripts/buildings.py 50.303376 30.217896 50.602416 30.841370`

Output will be located in `out.geojson`
