function updateSlide(n)
{
    displaySlide(slideIndex += n);
}

function displaySlide(n)
{
    var slides = document.getElementsByClassName("slideshow");
    if (n > slides.length - 1)
    {
        slideIndex = 0;
    }
    else if (n < 0)
    {
        slideIndex = slides.length - 1;
    }

    //loop through every slide and make them hidden
    var i;
    for (i = 0; i < slides.length; i++)
    {
        slides[i].style.display = "none";
    }
    //make the current slide display
    slides[slideIndex].style.display = "block";

    
}
