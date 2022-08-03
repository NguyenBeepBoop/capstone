const items = document.querySelectorAll('.sidebar a');
var path = window.location.href
items.forEach(item => {
    if(item.href === path) {
        item.classList.add('active');
    }
});