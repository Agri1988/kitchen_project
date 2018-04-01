$(document).ready(function detail_document () {
    if ($('#id_document_status').prop("checked")) {
        $('#id_document_type').click(function (e) {
                e.preventDefault()
                alert('Отмените проведение документа')
            });
        $('#id_date').click(function (e) {
                e.preventDefault()
                alert('Отмените проведение документа')
            });
        $('#table img').each(function () {
            $(this).click(function (e) {
                e.preventDefault()
                alert('Отмените проведение документа')
            })
        })
    }

    var doc_type = $('#id_document_type')
    doc_type.on('change', function () {
        change_btn_value()
    });
    function set_disabled() {
        $('#table tr').each(function () {
        $(this).find('#id_data').prop('disabled', 'true')
        $(this).find('#id_count').prop('disabled', 'true')
            });
    }
    set_disabled()

    function change_btn_value() {
        if ($('#id_document_type').val() == 0){
            $('#add_product_or_dish_btn').html("Добавить продукт")
        }
        else if ($('#id_document_type').val() == 1){
            $('#add_product_or_dish_btn').html("Добавить блюдо")
        }

    }
    change_btn_value()

});