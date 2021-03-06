function cloneMore(selector, type) {
    var newElement = $(selector).clone(true);
    var total = $('#id_' + type + '-TOTAL_FORMS').val();
    newElement.find(':input:not(button)').each(function () {
        var name = $(this).attr('name').replace('-' + (total - 1) + '-', '-' + total + '-');
        var id = 'id_' + name;
        $(this).attr({ 'name': name, 'id': id }).val('').removeAttr('checked');
    });
    newElement.find('label').each(function () {
        var newFor = $(this).attr('for').replace('-' + (total - 1) + '-', '-' + total + '-');
        $(this).attr('for', newFor);
    });
    total++;
    $('#id_' + type + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
    // var conditionRow = $('.form-row:not(:last)');
    // conditionRow.find('.btn.add-form-row')
    //             .removeClass('btn-success').addClass('btn-danger')
    //             .removeClass('add-form-row').addClass('remove-form-row')
    //             .html('-');

    //$('.form-row:not(:last)').find('.input-group-append').remove();

    // initialize autocomplete
    // if ( newElement.find( ".textSearch" ).autocomplete("instance") ){
    //     newElement.find( ".textSearch" ).autocomplete("destroy");
    //     newElement.find( ".textSearch").removeData("uiAutocomplete");
    // }
    //newElement.find( ".textSearch" ).autocomplete(autocompleteOptions);
}

function cloneAutocompleteRow( selector, type ) {
    let lastRowSelector = selector + ":last";
    if ( $(lastRowSelector).find( ".textSearch" ).autocomplete("instance") ){
        $(lastRowSelector).find( ".textSearch" ).autocomplete("destroy");
        $(lastRowSelector).find( ".textSearch").removeData("uiAutocomplete");
    }
    let prevLastRow = $(lastRowSelector);
    cloneMore( lastRowSelector, type )
    $(lastRowSelector).find(".textSearch").autocomplete(autocompleteOptions);
    $(prevLastRow).find(".textSearch").autocomplete(autocompleteOptions);
}

var autocompleteOptions = {
    minLength: 2,
    source: function(request, response) {
        $.ajax({
        type: "GET",
        url: "/ajax/search/",
        data: { term: request.term },
        success: function(data) {
            response(data);
        }
        });
    },
    response: function (event, ui) {
        if (!ui.content.length) {
            var noResult = { value: "", label: "Sorry, no movies found..." };
            ui.content.push(noResult);
        }
    }
}