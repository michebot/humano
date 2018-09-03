let modal = document.querySelector(".modal");
let closeButton = document.querySelector(".close");
let saveButton = document.querySelector(".save");

function toggleModal() {
    modal.classList.toggle("show-modal");
}

function windowOnClick(event) {
    if (event.target === modal) {
        toggleModal();
    }
}