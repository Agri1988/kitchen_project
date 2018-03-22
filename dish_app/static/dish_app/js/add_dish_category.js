function add_category () {
    console.log('add_category_product_form')
    var category = $('#id_category');
    category.after('<div id="modal_form_category">' +
        '<span id="modal_close_category">X</span>' +
        '</div>' +
        '<div id="overlay_category"></div>' +
            '<div class="form-group">' +
        '<button class="form-control" value="'+add_product_category+'" id="add_standart">Добавить категорию</button>' +
        '</div>');
    var add_btn = $('#add_standart');
    add_btn.click( function (e) {
        e.preventDefault();
        var data_dict= {};
        $('#product_detail_form p').each(function (index) {
            data_dict[index] = $(this).find('input').val()
        });
        $('#overlay_category').fadeIn(400, // снaчaлa плaвнo пoкaзывaем темную пoдлoжку
		 	function() { // пoсле выпoлнения предъидущей aнимaции
                $('#modal_form_category')
                    .css('display', 'block') // убирaем у мoдaльнoгo oкнa display: none;
                    .animate({opacity: 1, top: '50%'}, 200); // плaвнo прибaвляем прoзрaчнoсть oднoвременнo сo съезжaнием вниз
            });
        $.ajax({
                url:add_btn.val(),
                type:'GET',
                data:data_dict,
                cache:true,
                success:function (data){
                    console.log('OK');
                    console.log(data);
                    $('#modal_form_category').append(data)
                },
                error:function () {
                    console.log('error')
                }
            });

    });

    	/* Зaкрытие мoдaльнoгo oкнa, тут делaем тo же сaмoе нo в oбрaтнoм пoрядке */
    function close_modal_window () {
        $('#modal_form_category')
        .animate({opacity: 0, top: '45%'}, 200,  // плaвнo меняем прoзрaчнoсть нa 0 и oднoвременнo двигaем oкнo вверх
            function(){ // пoсле aнимaции
                $(this).css('display', 'none'); // делaем ему display: none;
                $('#overlay_category').fadeOut(400); // скрывaем пoдлoжку
                }
             );
        $('#modal_form_category').find('div').remove()
    }

	$('#modal_close_category, #overlay_category').click( function(){ // лoвим клик пo крестику или пoдлoжке
        close_modal_window()
	});

    $('#modal_form_category').on('submit',function (event) {
        event.preventDefault();
        var data_dict= {};
        $('#modal_form_category').find('#product_category_form div').each(function (index) {
            data_dict[$(this).find('input').attr('name')] = $(this).find('input').val()
        });
        data_dict['csrfmiddlewaretoken']=csrf;
        var url = $('#modal_form_category').find('#product_category_form').attr('action');
        console.log(data_dict);
        $.ajax({
                url:url,
                type:'POST',
                data:data_dict,
                cache:true,
                success:function (data){
                    console.log('OK', data);
                    var category = $('#id_category');
                    category.append("<option value="+data['new_element_id']+">"+data['new_element_name']+"</option>");
                    category.val(data['new_element_id']);
                    close_modal_window()
                },
                error:function () {
                    console.log('error')
                }
            });
    });
}/**
 * Created by Ar on 01.02.2018.
 */
