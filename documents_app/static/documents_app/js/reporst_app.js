/**
 * Created by Ar on 26.11.2017.
 */
$(document).ready(function () {
    var table = $('#table').find('tbody').find('th');
    var rows_length = document.getElementsByTagName('tr').length;

    function filter_data(index, sample) {
            var table = document.getElementById('table');
            for (var i = 2; i < rows_length; i++) {
                if ((table.rows[i].cells[index].innerText.toLowerCase()).indexOf(sample.toLowerCase()) == -1) {
                    table.rows[i].setAttribute("style", "display:none")
                }
                else if(sample != ''){table.rows[i].setAttribute("style", "display:")}
                else {
                    table.rows[i].setAttribute("style", "display:")
                }
            }
        }
    table.each(function (index) {
        var input = $(this).find('input');
            input.on('input keyup', function (e) {
                console.log(input.val());
                filter_data(index, String(input.val()))
            })
    });


    var get_remnants_form = $('#get_remnants_for_input_date');
    var get_remnants_btn = get_remnants_form.find('button');
    var get_remnants_date = get_remnants_form.find('#id_date_to');
    var get_remnants_storage = get_remnants_form.find('#id_storage');
    get_remnants_storage.append('<option value="0" selected="">Все склады</option>');
    get_remnants_storage.val('0');
    function create_url() {
            return get_remnants_form.attr('action')+get_remnants_date.val()+'/'

    }
    var csrf = get_remnants_form.find("[name='csrfmiddlewaretoken']").val();
    get_remnants_btn.on('click', function (event) {
        event.preventDefault();
        $.ajax({
                url: create_url(),
                type: 'POST',
                cache: true,
                data:{csrfmiddlewaretoken: csrf, ajax:true},
                success: function (data) {
                    console.log('OK');
                    $('.table-responsive ').remove();
                    $('.col-lg-8').append(data);
                    console.log(data);
                },
                error: function () {
                    console.log('error')
                }
            });
    })
});