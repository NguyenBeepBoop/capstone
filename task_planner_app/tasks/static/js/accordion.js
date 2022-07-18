function closeAllAccordians() {
    $(".accordion-label").each(function( index ) {
        $(this).removeClass("is-selected");
        $(this).ariaSelected = false;
    })
    
    $(".accordion-content").each(function( index ) {
        $(this).removeClass("is-open");
        $(this).addClass("is-closed");
        $(this).ariaSelected = false;
    })
}

function openAllAccordians() {
    $(".accordion-label").each(function( index ) {
        $(this).addClass("is-selected");
        $(this).ariaSelected = true;
    })
    
    $(".accordion-content").each(function( index ) {
        $(this).addClass("is-open");
        $(this).removeClass("is-closed");
        $(this).ariaSelected = true;
    })
}

$(document).ready( function() {
    $('.js-accordion').accordion();
    $("#close-all-accordions").on("click", closeAllAccordians)
    $("#open-all-accordions").on("click", openAllAccordians)
})