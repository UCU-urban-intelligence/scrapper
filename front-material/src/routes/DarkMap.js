import React, { Component } from 'react';
import ReactMap, { GeoJSONLayer, Popup } from 'react-mapbox-gl';

const accessToken = "pk.eyJ1Ijoic2VyaGlpLXRpdXRpdW5uaWsiLCJhIjoiY2pvcmZwcjJoMGJvaDNqczB5YTFiZWEzayJ9.hkUhm-xaZeZjBeVHOSFnOw";
const style = "mapbox://styles/mapbox/dark-v9";

const Map = ReactMap({ accessToken });

const mapStyle = {
  height: `100%`,
  width: `100%`
};

// const montreal = [-73.567256, 45.5016889];
const toronto = [-79.392464, 43.664317];

class DarkMap extends Component {

  constructor(props) {
    super(props);

    this.state = {
      // geojson: {},
      colors: ["#c51b7d", "#de77ae", "#f1b6da", "#fde0ef", "#e6f5d0", "#b8e186", "#7fbc41", "#4d9221"],
      popupData: undefined
    }
  }

  // componentDidMount() {
  //   fetch('/out__Toronto.geojson')
  //   .then(response => {
  //     return response.json()
  //   })
  //   .then(geojson => {
  //     console.log(geojson);
  //     this.setState({
  //       geojson
  //     })
  //   })
  // }

  _getColorGradient(features, colors) {
    const result = [];
    const bounds = [0, 5.77, 6.06, 6.28, 6.52, 6.8, 7.3, 8.98];
    for (let i = 0; i < bounds.length; i++) {
      result.push(bounds[i], colors[i])
    }

    return result
  }

  render() {

    const { colors, popupData } = this.state;
    const { geojson } = this.props;
    return (
      <Map
        style={style}
        containerStyle={mapStyle}
        zoom={[13]}
        center={toronto}
        pitch={[60]} // pitch in degrees
      >
        {!geojson.features || <GeoJSONLayer
          data={geojson}

          fillExtrusionLayout={{

          }}

          layerOptions={{
            paint: {
              'fill-extrusion-color': [
                'interpolate',
                ['linear'],
                ['get', 'efficiency']
              ].concat(this._getColorGradient(geojson.features, colors)),

              'fill-extrusion-height': {
                type: 'identity',
                property: 'height'
              },
              'fill-extrusion-base': {
                type:  'identity',
                property: 'min_height'
              },
              'fill-extrusion-opacity': 1
            }
          }}
          fillExtrusionOnClick={e => {
            this.setState({
              popupData: {
                ...e.features[0].properties,
                coordinates: [e.lngLat.lng, e.lngLat.lat]
              }
            });
            this.props.updateFeatures(e.features[0].properties)
          }}
        />}
        {!popupData || <Popup coordinates={popupData.coordinates} closeButton={true} closeOnClick={false} anchor="bottom">
          <div style={{ width: '160px' }}>
            {(() => {
              const data = ['efficiency'];
              for(let i in popupData) {
                if(['coordinates', 'efficiency'].indexOf(i) !== -1) continue;
                data.push(i)
              }
              return (data.map(item => {
                return (
                  <div key={item}>
                    <span>{(item[0].toUpperCase() + item.substr(1)).split('_').join(' ')}:</span>
                    <span style={{ float: 'right' }}>{Math.round(popupData[item]*1000)/1000}</span>
                  </div>
                )
              }))
            })()}
          </div>
        </Popup>}

      </Map>
    );
  }
}

export default DarkMap;
