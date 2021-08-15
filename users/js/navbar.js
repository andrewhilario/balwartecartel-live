const navSlide = ()=>{
    const burger = document.querySelector('.burger');
    const nav = document.querySelector('.navLink');
  
    burger.onclick = ()=>{
      nav.classList.toggle('navLinks-active');
  
      burger.classList.toggle('toggle');
    }
    window.onscroll = ()=>{
      if(pageYOffset >= 1000 ){
        nav.classList.toggle('navLinks-active');
        burger.classList.toggle('toggle');
      }
    }
  
  }
  navSlide();