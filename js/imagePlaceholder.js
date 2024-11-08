const images = document.querySelectorAll('img');
images.forEach(img => {
    img.onerror = function() {
        img.src = '../js/default_image.jpg';
        img.alt = "Default image";
        img.onerror = null; // No infinite loop if default image is also missing
        };
        
});