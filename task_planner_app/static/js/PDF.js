function submitPDF(data) {
    var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
    $.ajax({
        url: "pdf_page/pdf_view/", 
        type: "GET",
        headers: {
            'X-CSRFToken': csrftoken,
        },
        data: data,
        dataType: 'json',
    });
}

$('#pdf').click(function(event) {
    event.preventDefault();
    submitPDF();
    data = {
        group : $('#div_id_group')[0].value,
        user : $('div_id_user')[0].value,
        
    }
})