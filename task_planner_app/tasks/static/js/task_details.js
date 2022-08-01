function submit(data) {
    var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
    $.ajax({
        url: "/tasks/edit", 
        type: "POST",
        headers: {
            'X-CSRFToken': csrftoken,
        },
        data: data,
        dataType: 'json',
    });
}

$('#edit').click(function(event) {
    event.preventDefault();
    submit();
    location.reload()
})


function addComment(data) {
    var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
    $.ajax({
        url: "/tasks/edit", 
        type: "POST",
        headers: {
            'X-CSRFToken': csrftoken,
        },
        data: data,
        dataType: 'json',
    });
}

$('#comment-button').click(function(event) {
    event.preventDefault();
    data = {
        content: $(['name^=content'])[0].value,
    }
    addComment(data);
    location.reload()
})

function getPriority(data) {
    $.ajax({
        url: "/tasks/text", 
        type: "GET",
        data: data,
        dataType: 'json',
    });
}

$('#priority-btn').click(function(event) {
    event.preventDefault();
    data = {
        task_id: $("#task-id")[0].value,
    }
    console.log(data)
    getPriority(data);
})