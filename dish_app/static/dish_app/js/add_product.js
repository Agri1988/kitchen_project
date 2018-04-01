function add_product_script() {
    var id_field = '#add_new_product_btn';
    var id_form = '#table';
    var id_add_form = '#ingredient_form';
    var id_add_button = '#add_new_product_btn';
    var standart = $('#add_new_product_btn');
    standart.after('<div id="modal_form_product">' +
        '<span id="modal_close_product">X</span>' +
        '</div>' +
        '<div id="overlay_product"></div>')
    var add_btn = $(id_add_button);

        $('#overlay_product').fadeIn(400, // снaчaлa плaвнo пoкaзывaем темную пoдлoжку
		 	function() { // пoсле выпoлнения предъидущей aнимaции
                $('#modal_form_product')
                    .css('display', 'block') // убирaем у мoдaльнoгo oкнa display: none;
                    .animate({opacity: 1, top: '30%'}, 200); // плaвнo прибaвляем прoзрaчнoсть oднoвременнo сo съезжaнием вниз
            });
        console.log('dsfghjkhfsdadfghj')
        var csrf = $(document).find("[name='csrfmiddlewaretoken']").val();
        $.ajax({
                url:add_btn.val(),
                type:'GET',
                data:{ajax:'True'},
                cache:true,
                success:function (data){
                    console.log('OK');
                    console.log(data);
                    $('#modal_form_product').append(data)
                    //add_category()
                },
                error:function () {
                    console.log('error')
                }
            });





	$('#modal_close_product, #overlay_product').click( function(){ // лoвим клик пo крестику или пoдлoжке
        close_modal_window_product()
        $(this).fadeOut(400)
	});

};
/* Зaкрытие мoдaльнoгo oкнa, тут делaем тo же сaмoе нo в oбрaтнoм пoрядке */
    function close_modal_window_product () {
        $('#modal_form_product')
        .animate({opacity: 0, top: '45%'}, 200,  // плaвнo меняем прoзрaчнoсть нa 0 и oднoвременнo двигaем oкнo вверх
            function(){ // пoсле aнимaции
                $(this).css('display', 'none'); // делaем ему display: none;
                $('#overlay_product').fadeOut(400); // скрывaем пoдлoжку
                }
             );
        $('#modal_form_product').find('div').remove()

    }

function add_product_to_product_list(e) {
    e.preventDefault()
    var product_name = $('#modal_form_product').find('#id_name').val();
    var product_unit = $('#modal_form_product').find('#id_unit').val();
    var product_category = $('#modal_form_product').find('#id_category').val();
    console.log(product_name, product_unit)
    $.ajax({
        url:'/dishes/product_to_productList/',
        type:'POST',
        data:{csrfmiddlewaretoken:csrf, name:product_name, unit:product_unit, category:product_category, ajax:'True',
        line_number:(typeof(productlist_to_dish) === 'undefined') ? '' : productlist_to_dish},
        success:function (data){
            console.log('OK');
            console.log(data);
            $('#table_products').append(data)
            close_modal_window_product()
        },
        error:function () {
            console.log('error')
        }
    })

}