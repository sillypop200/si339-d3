const images = document.querySelectorAll('img');
images.forEach(img => {
    console.log("runs");
    img.onerror = function() {
         console.log("helo");
        img.src = '../js/default_image.jpg';
        img.alt = "Default image";
        img.onerror = null; // No infinite loop if default image is also missing
        };
        
});