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