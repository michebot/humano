// code to render map with location

let myLatLng = {lat: -34, lng: 151};
let map;
let user = $("#user").val();
// BEGIN code to render address
// let geocoder;
// let latitude = $("#lat").val();
// let longitude = $("#lng").val();
// console.log(latitude);
// console.log(longitude);
// let latLng = {lat: latitude, lng: longitude}
// END code to render address


function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: myLatLng,
    zoom: 15
  });

  $.get("/map-coordinates.json", {user_id: user}, function(data){
    myLatLng = new google.maps.LatLng(data);
    // geocoder = new google.maps.Geocoder;
    map.setCenter(myLatLng); 
    // console.log(data);
    // console.log(myLatLng);

    let marker = new google.maps.Marker({
    position: myLatLng,
    map: map,
    title: "I'm here"
    });
  });
}


// DEPRECATED: moved to google_js_map_api_call.py
// continue:code to render address 
// function geocodeLatLng(geocoder, infowindow) {
//   geocoder.geocode({'location': latLng}, function(results, status) {
//     console.log(results)
//     if (status === 'OK') {
//       if (results[0]) {
//         $("#address").html(results[0].formatted_address);
//         console.log(results[0].formatted_address)
//       } else {
//         window.alert('No results found');
//       }
//     } else {
//       window.alert('Geocoder failed due to: ' + status);
//     }
//   })
// };

