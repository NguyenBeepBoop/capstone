$(document).ready(function() {
    $('.spinner-border').hide();
});

function getResults(event, data) {
    var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
    $.ajax({
        url: "/dashboard/get_help/", 
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: data,
        dataType: 'json',
        cache: true,
        success: function(data) {
            $('.spinner-border').hide();
            showResults(data)
        }
    });
}


$('.help-btn').click(function(event) {
    btn_id = event.target.id;
    event.preventDefault();
    task_id = $(`#${btn_id}`)[0].value
    if ($(`#collapse-task-${task_id}`).hasClass("show") == false) {
        $('.spinner-border').show();
        data = {
            task_id: task_id,
        }
        getResults(event, data);
    }
})

function showResults(data) {
    var task_id = data.task_id
    const search_results = data.search_results
    if($(`#card-${task_id}`).children().length == 0) {   
        for (const res in search_results) {
            $(`#card-${task_id}`).append(
                `<div style="margin-bottom: 3px; padding-bottom: 3px;"> <a href="${search_results[res].link}">${search_results[res].title}</a> \
                </div>`
            )
        }
    }
}