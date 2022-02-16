$(document).ready(function() {
    $('#responsive').lightSlider({
        item:5,
        loop:false,
        slideMove:1,
        adaptiveHeight:true,
        slideMargin:20,
        easing: 'cubic-bezier(0.25, 0, 0.25, 1)',
        speed:600,
        responsive : [
            {
                breakpoint:992,
                settings: {
                    item:3,
                    slideMove:1,
                  }
            },
            {
                breakpoint:768,
                settings: {
                    item:2,
                    slideMove:1
                  }
            },
            {
                breakpoint:576,
                settings: {
                    item:1,
                    slideMove:1,
                  }
            },
        ]
    });  
  });
