$(document).ready(function () {
    var form = $('#get_report_day_income');
    var table = $('#table');
    var date = $('#id_date_to');
    var btn = $('#btn_submit');
    btn.click(function (event) {
        event.preventDefault()
        $.ajax({
            url: form.attr('action'),
            type:'POST',
            cache:true,
            data:{csrfmiddlewaretoken: csrf, ajax:true, date:date.val()},
            success: function (data) {
                    console.log('OK');
                    console.log(data);
                    table.append(data)
                },
                error: function () {
                    console.log('error')
                }
        })
    })
})