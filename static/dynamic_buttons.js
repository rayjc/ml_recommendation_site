function cloneMore(selector, type) {
    var newElement = $(selector).clone(true);
    var total = $('#id_' + type + '-TOTAL_FORMS').val();
    newElement.find(':input:not(:button)').each(function () {
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
}