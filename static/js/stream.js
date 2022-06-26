let cards = document.getElementsByClassName('card');
let datas = document.getElementsByClassName('data');

window.addEventListener("keydown", checkKeyPressed, false);

console.log(JSON.parse(datas[0].innerHTML)['image_uris']['png'])
console.log(typeof datas[0].innerHTML)

for (let i = 0; i < 10; i++) {
  cards[i].src = findImgUri(JSON.parse(datas[i].innerHTML))
}

function findImgUri(data) {
  return data['image_uris']['png']
}

function save() {
  sendData(1)
  cards[0].style.transform       = 'scale(0.0)';
  cards[0].style.height          = '0.0';
  cards[0].style.transformOrigin = 'right center';
  setTimeout(deleteCard1, 480);
  cards = document.getElementsByClassName('card');
};

function dismiss() {
  sendData(0)
  cards[0].style.transform       = 'scale(0.0)';
  cards[0].style.height          = '0.0';
  cards[0].style.transformOrigin = 'left center';
  setTimeout(deleteCard1, 480);
  cards = document.getElementsByClassName('card');
}

function deleteCard1() {
  cards[0].remove()
  datas[0].remove()
}

function newBatch() {
  var request = new XMLHttpRequest()
  request.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      let response = JSON.parse(request.responseText)
      for (i = 0; i < response.length; i++) {
        let newImg = document.createElement('img')
        newImg.classList.add('card')
        newImg.src = findImgUri(response[i])
        document.getElementsByClassName('container')[0].appendChild(newImg)
        let newData = document.createElement('div')
        newData.classList.add('data')
        newData.innerHTML = JSON.stringify(response[i])
        newData.style.visibility = "hidden"
        newData.style.height = '0'
        document.getElementsByClassName('container')[0].appendChild(newData)
      }
    }
  }
  request.open("GET", "/api/new_cmdrs/", true);
  request.send();
}

function sendData(good) {
  var request = new XMLHttpRequest()
  request.open("POST", `/set/${good}/${ datas[0].innerHTML }`)
  request.send()
}


function checkKeyPressed(evt) { 
  if (evt.keyCode == "37") { 
    dismiss();
  }; 
  if (evt.keyCode == "39") {
    save();
  };
  if (cards.length <= 5) {
    console.log('o')
    newBatch()
  };
};