// Deleting a contact modal

// $("#remove-contact-").on("click", function(evt){
$(".remove-contact").on("click", function(evt){
  evt.preventDefault();
  $("#deleteModal").modal("toggle");
});

let route = $("#contact").val();

function Delete(){
  $.post(route,
         {},
         () => {
           $("#deleteModal").modal("hide");
           location.reload();
         });
}