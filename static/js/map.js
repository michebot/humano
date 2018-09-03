let myLatLng = {lat: -34, lng: 151};
let map;
let user = $("#user").val();

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: myLatLng,
    zoom: 15
  });

  $.get("/map-coordinates.json", {user_id: user}, function(data){
    myLatLng = new google.maps.LatLng(data);
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