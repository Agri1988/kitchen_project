$(document).ready(function add_dish_foo() {
    var btn = $('#add_product_or_dish_btn');
    btn.after('<div id="modal_form">' +
        '<span id="modal_close">X</span>' +
        '</div>' +
        '<div id="overlay"></div>');
    var add_btn = $('#add_product_or_dish_btn');
    add_btn.click( function (e) {
        e.preventDefault();
        if ($('#id_document_status').prop("checked")) {
            alert('Отмените проведение документа')
        }
        else {
            $('#overlay').fadeIn(400, // снaчaлa плaвнo пoкaзывaем темную пoдлoжку
                function () { // пoсле выпoлнения предъидущей aнимaции
                    $('#modal_form')
                        .css('display', 'block') // убирaем у мoдaльнoгo oкнa display: none;
                        .animate({opacity: 1, top: '50%'}, 200); // плaвнo прибaвляем прoзрaчнoсть oднoвременнo сo съезжaнием вниз
                });
        }

        if ($('#id_document_type').val() == 1) {
            console.log('invoice')
            $.ajax({
                url: '/documents/get_all_dishes_to_document/',
                type: 'GET',
                data: {},
                cache: true,
                success: function (data) {
                    console.log('OK');
                    // console.log(data);
                    $('#modal_form').append(data)
                },
                error: function () {
                    console.log('error')
                }
            });
        }
        else if ($('#id_document_type').val() != 1) {
            $.ajax({
                url:'/documents/get_all_products_to_document/',
                type:'GET',
                data:{modal:'True'},
                cache:true,
                success:function (data){
                    console.log('OK');
                    // console.log(data);
                    $('#modal_form').append(data);
                    show_remnants_foo()

                    // $('#modal_form').append('<input class="btn btn-dark" id="add_new_product_btn" value="Добавить продукт" type="button">')
                },
                error:function () {
                    console.log('error')
                }
            });
        }


    });

    	/* Зaкрытие мoдaльнoгo oкнa, тут делaем тo же сaмoе нo в oбрaтнoм пoрядке */
    function close_modal_window () {
        $('#modal_form')
        .animate({opacity: 0, top: '45%'}, 200,  // плaвнo меняем прoзрaчнoсть нa 0 и oднoвременнo двигaем oкнo вверх
            function(){ // пoсле aнимaции
                $(this).css('display', 'none'); // делaем ему display: none;
                $('#overlay').fadeOut(400); // скрывaем пoдлoжку
                }
             );
        $('#modal_form').find('div').remove()
    }

	$('#modal_close, #overlay').click( function(){ // лoвим клик пo крестику или пoдлoжке
        close_modal_window()
	});
    function show_remnants_foo() {
        $('#table_dishes tr').each(function () {
            var this_row = $(this).find('#show_remnants');
            var product_id =  $(this).find('#send_btn').val();
            var count = $(this).find('input');
            count.focusin(function () {
                $.ajax({
                    url:'/documents/products_remnants/',
                    type:'GET',
                    data:{ajax:'True', product_id:product_id},
                    cache:true,
                    success:function (data){
                        console.log('OK');
                        console.log(data[product_id]);
                        this_row.append('<div>доступно<br>'+data[product_id]+'</div>');
                        this_row.show()
                        // $('#modal_form').append('<input class="btn btn-dark" id="add_new_product_btn" value="Добавить продукт" type="button">')
                    },
                    error:function () {
                        console.log('error')
                    }
                });

            });
            count.focusout(function () {
                this_row.find('div').remove();
                this_row.hide()
            })
        })
    }
})/**
 * Created by Ar on 01.02.2018.
 */
