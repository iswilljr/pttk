let button_menuBar = document.querySelector('.bx-menu')
let menuBar = document.querySelector('.menu-responsive')

button_menuBar.onclick = function () {
    menuBar.classList.toggle('active')
}

//frontpage 
let opc = document.querySelectorAll(".fa-ellipsis-h");
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

function file_img() {
    var archivo = document.getElementById("fileImg").files[0];
    var reader = new FileReader();
    if (fileImg) {
        reader.readAsDataURL(archivo);
        reader.onloadend = function () {
            document.getElementById("imgs").className = "img active"
            document.getElementById("vids").className = "vid"
            document.getElementById("imgs").src = reader.result;
        }
    }
}
function file_vid() {
    var archivo = document.getElementById("fileVid").files[0];
    var reader = new FileReader();
    if (fileVid) {
        reader.readAsDataURL(archivo);
        reader.onloadend = function () {
            document.getElementById("vids").className = "vid active"
            document.getElementById("imgs").className = "img"
            document.getElementById("vids").src = reader.result;
        }
    }
}

let btnsPost = document.querySelectorAll('.btn-dlt-pst')
btnsPost.forEach(btn => {
    btn.onclick = e=>{
        if(!confirm('Seguro que quiere eliminar el post?')){
            e.preventDefault()
            opcs.forEach(opc => {
                opc.className = "op-menu"
            });
        }
    }
});

let formComt = document.querySelectorAll('.comt-btn')
let btnComt = document.querySelectorAll('.btn-comt')
let Comt = document.querySelectorAll('.comt-msgs')
for(let btn in btnComt){
    btnComt[btn].onclick = function(){
        Comt[btn].classList.toggle('active')
        formComt[btn].classList.toggle('active')
    }
}

let btnDeltComt = document.querySelectorAll('.delt-comt')
btnDeltComt.forEach(btn => {
    btn.onclick = e=>{
        if(!confirm('¿Está seguro de eliminar del comentario?')){
            e.preventDefault()
        }
    }
});
let btnEditComt = document.querySelectorAll('.edit-comt')
let postComt = document.querySelectorAll('.txta-comt')
let comtArea = document.querySelectorAll('.editar-comt-post')
for(let btn in btnEditComt){
    btnEditComt[btn].onclick = function(){
        postComt[btn].setAttribute('style','display: block;')
        comtArea[btn].setAttribute('style','display: none;')
        btnEditComt.forEach(btn => {
            btn.setAttribute('style','display: none;')
        });
    }
}

let btnCantEditComt = document.querySelectorAll('.btn-can-comt')


for(let i in btnCantEditComt){
    btnCantEditComt[i].onclick = e=>{
        e.preventDefault()
        btnEditComt.forEach(btn => {
            btn.setAttribute('style','display: inline;')
        });
        postComt[i].setAttribute('style','display: none;')
        comtArea[i].setAttribute('style','display: block;')
    }
}

// frontpage end



//user profile
let list = document.querySelectorAll('.item-user');
let listC = document.querySelectorAll('.content-user')
let cont = document.querySelector(".contenido");
for (let i = 0; i < list.length; i++) {
    list[i].onclick = function () {
        let j = 0;
        while (j < list.length) {
            if (list[j].className == 'item-user fotos' || list[j].className == 'item-user fotos select') {
                list[j].className = 'item-user fotos'
            } else {
                list[j].className = 'item-user'
            }
            listC[j].className = 'content-user'
            cont.className = 'contenido'
            j++;
        } if (list[i].className == 'item-user fotos') {
            list[i].className = 'item-user fotos select'
            cont.className = 'contenido active'
        } else {
            list[i].className = 'item-user select'
        }
        listC[i].className = 'content-user active'
    }
}

let chats = document.querySelectorAll('.user-chat-n');
let contChats = document.querySelectorAll('.cont-chat-n');
let backArrow = document.querySelectorAll('#back')
let contChat = document.querySelector('.contenido-chats')

for (let i = 0; i < chats.length; i++) {
    chats[i].onclick = function () {
        let j = 0;
        while (j < chats.length) {
            chats[j].className = 'user-chat-n';
            contChats[j].className = 'cont-chat-n';
            j++;
        } chats[i].className = 'user-chat-n select';
        contChats[i].className = 'cont-chat-n active';
        contChat.classList.toggle('on')
    }
    backArrow[i].onclick = function () {
        contChat.classList.toggle('on')
    }
}

let buttonEdit = document.querySelectorAll('.edit-cont')
let inputEdit = document.querySelectorAll('.input-edit-cont')
for (let i = 0; i < buttonEdit.length; i++) {
    let btn = buttonEdit[i];
    let ipt = inputEdit[i];
    let btnEdit = document.querySelector('.button-edit');
    btn.onclick = function () {
        btnEdit.className = 'button-edit active'
        let atr = ipt.getAttributeNames()
        for (let j = 0; j < atr.length; j++) {
            if (atr[j] == 'disabled') {
                ipt.removeAttribute('disabled')
            } else {
                ipt.setAttribute('disabled', 'disabled')
            }

        }

    }
}

function habilitar() {
    for (let i = 0; i < inputEdit.length; i++) {
        let ipt = inputEdit[i];
        ipt.removeAttribute('disabled')

    }
}


//user profile end

//dashboard
let dash_items = document.querySelectorAll(".dash-item");
let dash_conts = document.querySelectorAll(".dash-content-item")
let optionDash = document.querySelectorAll('.option-dash')
let consulta = document.getElementById('consulta')
for (let i = 0; i < dash_items.length; i++) {
    dash_items[i].onclick = function () {
        for (let k = 0; k < optionDash.length; k++) {
            optionDash[k].removeAttribute('selected');
        }
        let j = 0;
        while (j < dash_items.length) {
            dash_items[j].className = "dash-item";
            dash_conts[j].className = "dash-content-item";

            j++;
        }dash_items[i].className = "dash-item select";
        dash_conts[i].className = "dash-content-item active";
        if(i==0){
            if(optionDash[0]){
                optionDash[0].setAttribute('selected', 'selected')
            }
            if(consulta){
                consulta.setAttribute('placeholder','Ingresa el id de un post para modificarlo')
            }
            
        }else if(i==1){
            if(optionDash[1]){
                optionDash[1].setAttribute('selected','selected')
            }
            if(consulta){
                consulta.setAttribute('placeholder','Ingresa el id de un post para modificarlo')
            }
            
        }else if(i==2){
            if(optionDash[2]){
                optionDash[2].setAttribute('selected','selected')
            }
            if(consulta){
                consulta.setAttribute('placeholder','Ingresa un usuario para ver y modificar su contenido')
            }
            
        }else if(i==3){
            if(optionDash[3]){
                optionDash[3].setAttribute('selected','selected')
            }
            if(consulta){
                consulta.setAttribute('placeholder','Ingresa un usuario para ver y modificar su contenido')
            }
            
        }
    }
}

function actionSelect(){
    let selectDash = document.querySelector('.select-dash')
    let dashConsulta = document.getElementById('dashConsulta')
    if(selectDash.value=='post' || selectDash.value=='comt'){
        dashConsulta.action='/Dash/Post'
    }else if(selectDash.value=='user' || selectDash.value=='asig'){
        dashConsulta.action='/Dash/User'
    }
}

let buttonUserDash = document.querySelectorAll('.button-user-dash')
let contUserDash = document.querySelectorAll('.opciones-dash')
for (let i = 0; i < buttonUserDash.length; i++) {
    let btn = buttonUserDash[i];
    btn.onclick = function(){
        contUserDash[i].classList.toggle('active')
    }
    
}

let formRol = document.getElementById('formRol')
function user(){
    formRol.action="/Dash/User/Rol/USUARIO"
}
function admin(){
    formRol.action="/Dash/User/Rol/ADMINISTRADOR"
}
function superadmin(){
    formRol.action="/Dash/User/Rol/SUPERADMINISTRADOR"
}
// dashboard end


function flash(){
    let flashMenu = document.querySelector('.alert');
    flashMenu.className = "alert desactive";
}
