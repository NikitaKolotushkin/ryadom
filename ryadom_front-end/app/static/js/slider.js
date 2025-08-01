setInterval(() => {
    const slides = document.querySelectorAll('.slider__element');
    let active = document.querySelector('.slider__element.active');
    
    let index = Array.from(slides).indexOf(active);
    
    active.classList.remove('active');
    
    const nextIndex = (index + 1) % slides.length;
    slides[nextIndex].classList.add('active');
}, 3000);