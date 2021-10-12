let button_menuBar= document.querySelector('.bx-menu')
let menuBar = document.querySelector('.menu-responsive')

button_menuBar.onclick = function(){
    menuBar.classList.toggle('active')
}

//frontpage 
let opc = document.querySelectorAll(".op-button");
let opcs = document.querySelectorAll(".op-menu");

for (let i = 0; i < opc.length; i++) {
    opc[i].onclick = function () {
        let j = 0;
        while (j < opc.length) {
            if (opcs[j].className == "op-menu active" && opcs[i].className == "op-menu active") {
                opcs[i].className = "op-menu active";
            } else {
                opcs[j].className = "op-menu";
            }
            j++;
        } opcs[i].classList.toggle("active")
    }
}
// frontpage end



//user profile
let list = document.querySelectorAll('.item-user');
let listC = document.querySelectorAll('.content-user')
for(let i = 0; i < list.length; i++){
    list[i].onclick = function(){
        let j = 0;
        while(j < list.length){
            list[j].className = 'item-user'
            listC[j].className = 'content-user'
            j++;
        }list[i].className = 'item-user select'
        listC[i].className = 'content-user active'
    }
}
//user profile end

//dashboard
let dash_items = document.querySelectorAll(".dash-item");
let dash_conts = document.querySelectorAll(".dash-content-item")
for(let i = 0; i<dash_items.length; i++){
    dash_items[i].onclick = function(){
        let j = 0;
        while(j<dash_items.length){
            dash_items[j].className = "dash-item";
            dash_conts[j].className = "dash-content-item";
            j++;
        }dash_items[i].className = "dash-item select";
        dash_conts[i].className = "dash-content-item active";
    }
}
// dashboard end
