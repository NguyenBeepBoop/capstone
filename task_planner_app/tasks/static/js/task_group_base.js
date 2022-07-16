const items = document.querySelectorAll('.sidebar2 a');
var path = window.location.href
items .forEach(item => {
    console.log(item.href)
    console.log(path)
    if(item.href === path) {
        item.classList.add('active');
    }
});

function leaveUser(event, data) {
    var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
    $.ajax({
        url: "/group_members/leave", 
        type: "POST",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: data,
        dataType: 'json',
    });
}


$('#leave-btn').click(function(event) {
    btn_id = event.target.id;
    event.preventDefault();
    data = {
        user_id: $(`#${btn_id}`)[0].value,
        group_id: $('#group-id')[0].value,
    }
    leaveUser(event, data);
    window.location.replace("http://127.0.0.1:8000/groups/")
})
