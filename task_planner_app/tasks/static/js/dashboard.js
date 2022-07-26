function getResults(event, data) {
    var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
    $.ajax({
        url: "/dashboard/get_help/", 
        type: "POST",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: data,
        dataType: 'json',
    });
}


$('#help-btn').click(function(event) {
    btn_id = event.target.id;
    event.preventDefault();
    data = {
        task_id: $(`#${btn_id}`)[0].value,
    }
    getResults(event, data);
})

