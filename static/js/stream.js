const color_button = document.getElementById('color_cookie_push');
const type_button = document.getElementById('type_cookie_push');

let cookie_colors = decodeURI(document.getElementByClassName('cookie_colors')[0].id)
//console.log(document.getElementById('color_container').childNodes)
console.log(cookie_colors)

let cards = document.getElementsByClassName('card');
let right_swipe

window.addEventListener("keydown", checkKeyPressed, false);

function save() {
  cards[0].style.transform = 'scale(0.0)';
  cards[0].style.height = '0.0';
  cards[0].style.transformOrigin = 'right center';
  setTimeout(delete_card_1, 480);
  cards = document.getElementsByClassName('card');
};

function dismiss() {
  cards[0].style.transform = 'scale(0.0)';
  cards[0].style.height = '0.0';
  cards[0].style.transformOrigin = 'left center';
  setTimeout(delete_card_1, 480);
  cards = document.getElementsByClassName('card');
}

function delete_card_1() {
  cards[0].remove()
}

function checkKeyPressed(evt) { 
  if (evt.keyCode == "37") { 
    dismiss();
  }; 
  if (evt.keyCode == "39") {
    save();
  };
  if (cards.length <= 1) {
    color_button.click();
    type_button.click();
  };
};