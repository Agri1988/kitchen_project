$(document).ready(function detail_document () {
    if ($('#id_document_status').prop("checked")) {
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
    function send_data_to_view() {
        data = {}
        $('table tr').each(function () {
            console.log($(this).find('input').val())
        })
        $.ajax({
            url:'/documents/find_entry/',
            type:'GET',
            data:{text:'text'},
            cache:true,
            success:function (data){
                console.log('OK');
            },
            error:function () {
                console.log('error')
            }
        });
    }

    $('#table tr').each(function () {
        $(this).find('#id_data').prop('disabled', 'true')
        $(this).find('#id_count').prop('disabled', 'true')
            });
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