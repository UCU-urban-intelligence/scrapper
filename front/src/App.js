import React, { Component } from 'react';
import ReactMap from 'react-mapbox-gl';
import { Layer, Feature } from 'react-mapbox-gl';

const accessToken = "pk.eyJ1Ijoic2VyaGlpLXRpdXRpdW5uaWsiLCJhIjoiY2pvcmZwcjJoMGJvaDNqczB5YTFiZWEzayJ9.hkUhm-xaZeZjBeVHOSFnOw";
const style = "mapbox://styles/mapbox/dark-v9";

const Map = ReactMap({
  accessToken
});

const mapStyle = {
  height: '100vh',
  width: '100vw'
};

const kiev = [30.5238, 50.45466]

class App extends Component {
  render() {
    return (
      <Map
        style={style}
        containerStyle={mapStyle}
        center={kiev}
      >
        <Layer
          type="symbol"
          id="marker"
          layout={{ "icon-image": "marker-15" }}>
          <Feature coordinates={kiev}/>
        </Layer>
      </Map>

    );
  }
}

export default App;
