// PROMOTE FUNCTIONS
function promoteUser(event, data) {
    var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
    $.ajax({
        url: "/group_members/promote", 
        type: "POST",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: data,
        dataType: 'json',
    });
}


$('.promote').click(function(event) {
    btn_id = event.target.id;
    event.preventDefault();
    data = {
        user_id: $(`#${btn_id}`)[0].value,
        group_id: $('#group-id')[0].value,
    }
    promoteUser(event, data);
    location.reload()
})



// DEMOTE FUNCTIONS
function demoteUser(event, data) {
    var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
    $.ajax({
        url: "/group_members/demote", 
        type: "POST",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: data,
        dataType: 'json',
    });
}


$('.demote').click(function(event) {
    btn_id = event.target.id;
    event.preventDefault();
    data = {
        user_id: $(`#${btn_id}`)[0].value,
        group_id: $('#group-id')[0].value,
    }
    demoteUser(event, data);
    location.reload()
})


// KICK FUNCTIONS
function kickUser(event, data) {
    var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
    $.ajax({
        url: "/group_members/kick", 
        type: "POST",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: data,
        dataType: 'json',
    });
}


$('.kick').click(function(event) {
    btn_id = event.target.id;
    event.preventDefault();
    data = {
        user_id: $(`#${btn_id}`)[0].value,
        group_id: $('#group-id')[0].value,
    }
    kickUser(event, data);
    location.reload()
})
