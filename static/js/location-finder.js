// On click, this button will obtain the user's location and send the user's location and message to their contacts
$("#send-message-location").on("click", function(evt){
  navigator.geolocation.getCurrentPosition(savePosition, errorHandler);
});

function savePosition(position) {
  let userLocation = {
      "lat": position.coords.latitude,
      "lng": position.coords.longitude,
  };

  $.post("/send-message.json",
         userLocation,
         () => $('#exampleModalLong').modal('toggle'),
  );
}

// Report errors to user
function errorHandler(error) {
 switch (error.code) {
  case error.PERMISSION_DENIED:
    alert("Could not get position as permission was denied.");
    break;
  case error.POSITION_UNAVAILABLE:
    alert("Could not get position as this information is not available at this time.");
    break;
   case error.TIMEOUT:
     alert("Attempt to get position timed out.");
    break;
   default:
    alert("Sorry, an error occurred. Code: " + error.code + " Message: " + error.message);
    break;
   }
}
$('#exampleModalLong').on('hidden.bs.modal', function () {
location.reload();
})


// On click, will request user's location to search for lawyers
// $("#search-lawyers").on("click", function(evt){
//   navigator.geolocation.getCurrentPosition(getPosition, errorHandler);
// });

// function getPosition(position) {
//   let userLocation = {
//       "lat": position.coords.latitude,
//       "lng": position.coords.longitude,
//   };

//   $.post("/search-lawyers",
//          userLocation,
//          () => alert("Searching for lawyers!"),
//   );
// }