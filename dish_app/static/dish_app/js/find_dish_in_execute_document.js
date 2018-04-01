/**
 * Created by Ar on 30.03.2018.
 */
$(document).ready(function () {
    $('#table tr').click(function (e) {
        e.preventDefault();
        var ingredient_id = $(this).find('input').val()
        $.ajax({
                url:'/dishes/get_dish_in_documents/',
                type:'GET',
                data:{dish_id:dish_id},
                cache:true,
                success:function (data){
                    console.log('OK');
                    console.log(data.response);
                    if (data.response){
                        alert('Редактирование невозможно, блюдо находится в проведенных документах')
                    }
                    else {
                        document.location.href = '/dishes/detail_ingredient/'+dish_id+'/'+ ingredient_id+'/'
                    }
                },
                error:function () {
                    console.log('error')
                }
            });
    })
})
