const next = document.getElementById('next')
const prev = document.getElementById('prev')
const slider = document.querySelector('#movies .movies')
next.addEventListener('click',function () {
    const card = document.querySelector('.card')
    const width = card.offsetWidth
    slider.scrollLeft += width
    console.log(slider.scrollLeft)
})
prev.addEventListener('click',function () {
    const card = document.querySelector('.card')
    const width = card.offsetWidth
    slider.scrollLeft -= width
})

slider.addEventListener('scroll',function(){
    const card = document.querySelector('.card')
    const width = card.offsetWidth
    if (slider.scrollLeft>=(width/2) ){
        prev.disabled = false
    }else{
        prev.disabled = true
    };
    if (slider.scrollLeft > (width*(slider.childElementCount-1)-slider.offsetWidth)){
        next.disabled = true
    }else{next.disabled = false}
})