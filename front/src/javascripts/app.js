// initialize map
var map = L.map('map').setView([38, 0], 4);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, Imagery &copy; <a href="http://cloudmade.com">CloudMade</a>', maxZoom: 18}).addTo(map);

// add AreaSelect with keepAspectRatio:true
var areaSelect = L.areaSelect({
  width:100,
  height:150,
  keepAspectRatio:true
});
areaSelect.addTo(map);