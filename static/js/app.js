function goTop(){
    var click = document.getElementById("top");

    console.log(pageYOffset);
    window.onscroll = ()=>{
        if(pageYOffset >= 1000){
            // click.style.display = "flex";
            click.style.right = "20px";
        }else{
            // click.style.display = "none";
            click.style.right = "-100px";
        }
    }
}
goTop();

function products(){
  let products = document.getElementById("shop");

  products.onclick = ()=>{
    window.location.href = "/products";
  }
}
products();

// function onLoading(){
//     const h1 = document.querySelector("h1")


// }
// onLoading();
