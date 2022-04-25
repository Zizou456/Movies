$(window).load(function () {
    setTimeout(function(){$('#loading').hide();}, 3000);
});

$(document).ready(function () {
    $('.responsive').each(function () {
            $(this).lightSlider({
                item: 5,
                loop: false,
                slideMove: 1,
                // adaptiveHeight: true,
                slideMargin: 20,
                easing: 'cubic-bezier(0.25, 0, 0.25, 1)',
                speed: 600,
                responsive: [
                    {
                        breakpoint: 992,
                        settings: {
                            item: 3,
                            slideMove: 1,
                        }
                    },
                    {
                        breakpoint: 768,
                        settings: {
                            item: 2,
                            slideMove: 1
                        }
                    },
                    {
                        breakpoint: 576,
                        settings: {
                            item: 1,
                            slideMove: 1,
                        }
                    },
                ]
            });
        }
    )
});

var text_max = 210;
$('#count_message').html(text_max + ' remaining');
$('#bio').keyup(function () {
    var text_length = $('#bio').val().length;
    var text_remaining = text_max - text_length;
    $('#count_message').html(text_remaining + ' remaining');
});

const ctx = document.getElementById('myChart');
const myChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        datasets: [{
            label: '# of Votes',
            data: [12, 19, 3, 5, 2, 3],
            backgroundColor: [
                'rgba(255, 99, 132)',
                'rgba(54, 162, 235)',
                'rgba(255, 206, 86)',
                'rgba(75, 192, 192)',
                'rgba(153, 102, 255)',
                'rgba(255, 159, 64)'
            ],
            hoverOffset: 4
        }]
    },
    options: {
        plugins: {
            title: {
                display: true,
                text: 'Most Liked Categories',
                font: {
                    size: 20
                }
            },
            legend: {
                display: false,
                position: 'top',
                align: 'center'
            }
        }
    }
});

let dots = document.querySelector(".dots");

// Function
// ========
function animate(element, className) {
    element.classList.add(className);
    setTimeout(() => {
        element.classList.remove(className);
        setTimeout(() => {
            animate(element, className);
        }, 500);
    }, 2500);
}

// Execution
// =========
animate(dots, "dots--animate");

