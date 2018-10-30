// initialize map
var map = L.map('map').setView([38, 0], 4);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, Imagery &copy; <a href="http://cloudmade.com">CloudMade</a>', maxZoom: 18}).addTo(map);

// add AreaSelect with keepAspectRatio:true
var areaSelect = L.areaSelect({
  width:100,
  height:150,
  keepAspectRatio:false
});
console.log(areaSelect);
areaSelect.addTo(map);

function showLoader() {

}

function hideLoader() {

}

function fetchBBoxData(lng1, lat1, lng2, lat2) {
  return fetch("http://localhost:8000/processing", {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      "bbox": [lng1, lat1, lng2, lat2]
    })
  });
}

document.getElementById('detect').addEventListener('click', function () {
  const bbox = areaSelect.getBounds();
  showLoader();
  fetchBBoxData(bbox.getWest(), bbox.getSouth(), bbox.getEast(), bbox.getNorth())
    .catch(err => console.error(err))
    .then(hideLoader)
});