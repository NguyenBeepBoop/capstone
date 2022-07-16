const items = document.querySelectorAll('.sidebar2 a');
var path = window.location.href
items .forEach(item => {
    console.log(item.href)
    console.log(path)
    if(item.href === path) {
        item.classList.add('active');
    }
});