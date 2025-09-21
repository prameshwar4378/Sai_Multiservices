(function ($) {
    "use strict";
 

    // Header carousel
    $(".header-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1500,
        autoplayTimeout: 6000,
        lazyLoad:true,
        items: 1,
        dots: true,
        loop: true,
        nav : true,
        navText : [
            '<i class="bi bi-chevron-left"></i>',
            '<i class="bi bi-chevron-right"></i>'
        ]
    });


    $(window).scroll(function() {

      if (visible($('.count-digit'))) {
          if ($('.count-digit').hasClass('counter-loaded')) return;
          $('.count-digit').addClass('counter-loaded');

          $('.count-digit').each(function() {
              var $this = $(this);
              jQuery({
                  Counter: 0
              }).animate({
                  Counter: $this.text()
              }, {
                  duration: 3000,
                  easing: 'swing',
                  step: function() {
                      $this.text(Math.ceil(this.Counter));
                  }
              });
          });
      }
  })
  
})(jQuery);






const menu = document.querySelector(".menu");
const menuMain = menu.querySelector(".menu-main");
const goBack = menu.querySelector(".go-back");
const menuTrigger = document.querySelector(".mobile-menu-trigger");
const closeMenu = menu.querySelector(".mobile-menu-close");
let subMenu;
menuMain.addEventListener("click", (e) =>{
    if(!menu.classList.contains("active")){
        return;
    }
  if(e.target.closest(".menu-item-has-children")){
       const hasChildren = e.target.closest(".menu-item-has-children");
     showSubMenu(hasChildren);
  }
});
goBack.addEventListener("click",() =>{
     hideSubMenu();
})
menuTrigger.addEventListener("click",() =>{
     toggleMenu();
})
closeMenu.addEventListener("click",() =>{
     toggleMenu();
})
document.querySelector(".menu-overlay").addEventListener("click",() =>{
    toggleMenu();
})
function toggleMenu(){
    menu.classList.toggle("active");
    document.querySelector(".menu-overlay").classList.toggle("active");
}
function showSubMenu(hasChildren){
   subMenu = hasChildren.querySelector(".sub-menu");
   subMenu.classList.add("active");
   subMenu.style.animation = "slideLeft 0.5s ease forwards";
   const menuTitle = hasChildren.querySelector("i").parentNode.childNodes[0].textContent;
   menu.querySelector(".current-menu-title").innerHTML=menuTitle;
   menu.querySelector(".mobile-menu-head").classList.add("active");
}

function  hideSubMenu(){  
   subMenu.style.animation = "slideRight 0.5s ease forwards";
   setTimeout(() =>{
      subMenu.classList.remove("active");	
   },300); 
   menu.querySelector(".current-menu-title").innerHTML="";
   menu.querySelector(".mobile-menu-head").classList.remove("active");
}

window.onresize = function(){
    if(this.innerWidth >991){
        if(menu.classList.contains("active")){
            toggleMenu();
        }

    }
}

 

$(document).ready(function(){
  $(".gallery-carousel").owlCarousel({
    loop: true,
    margin: 10,
    stagePadding: 50,  // Adjust this value to control the visible portion of adjacent items
    autoplay: true,
    smartSpeed: 3000,
    autoplayHoverPause: false, 
    dots: true,
    center: true,
    responsive: {
      0: {
        items: 1,
        stagePadding: 30
      },
      600: {
        items: 2,
        stagePadding: 20
      },
      1000: {
        items: 3,
        stagePadding: 30
      },
      1200: {
        items: 4,
        stagePadding: 50
      }
    }
  });
});




$(document).ready(function(){
  $(".news-carousel").owlCarousel({
    loop: true,
    margin: 10,
    stagePadding: 50,  // Adjust this value to control the visible portion of adjacent items
    autoplay: true,
    smartSpeed: 3000,
    autoplayHoverPause: false, 
    dots: true,
    center: true,
    responsive: {
      0: {
        items: 1,
        stagePadding: 30
      },
      600: {
        items: 2,
        stagePadding: 20
      },
      1000: {
        items: 3,
        stagePadding: 30
      },
      1200: {
        items: 4,
        stagePadding: 50
      }
    }
  });
});




 
$(".news-carousel").owlCarousel({
  autoplay: true,
  smartSpeed: 1000,
  center: true,
  margin: 25,
  dots: true,
  loop: true,
  nav : false,
  responsive: {
      0:{
          items:1
      },
      576:{
          items:2
      },
      768:{
          items:3
      },
      992:{
          items:2
      },
      1200:{
          items:3
      }
  }


  
});


 
$(document).ready(function(){
  $(".about-gallery-carousel").owlCarousel({
      loop: true,
      margin: 10,
      items: 1, // Show only one item at a time
      stagePadding: 50, // Adjust this value to control the visible portion of adjacent items
      autoplay: true,
      smartSpeed: 3000,
      autoplayHoverPause: false,
      dots: true,
      center: false, // Center should be false to show only one image per slide
      responsive: {
          0: {
              items: 1,
              stagePadding: 20
          },
          600: {
              items: 1,
              stagePadding: 30
          },
          1000: {
              items: 1,
              stagePadding: 50
          },
          1200: {
              items: 1,
              stagePadding: 50
          }
      }
  });
}); 

 



$(document).ready(function(){
  $(".certificate-head-carousel").owlCarousel({
    loop: true,
    margin: 10,
    stagePadding: 50,  // Adjust this value to control the visible portion of adjacent items
    autoplay: true,
    smartSpeed: 3000,
    autoplayHoverPause: false, 
    dots: true,
    center: true,
    responsive: {
      0: {
        items: 1,
        stagePadding: 30
      },
      600: {
        items: 2,
        stagePadding: 20
      },
      1000: {
        items: 3,
        stagePadding: 30
      },
      1200: {
        items: 4,
        stagePadding: 50
      }
    }
  });
});


