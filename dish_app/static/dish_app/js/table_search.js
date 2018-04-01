/**
 * Created by Ar on 28.03.2018.
 */
function table_search(table_id) {
    var table_th = $('#'+table_id).find('tbody').find('th');
    var rows_length = document.getElementsByTagName('tr').length;
    var table = document.getElementById(table_id);
    function filter_data(index, sample) {
        for (var i = 1; i < rows_length; i++) {
            if ((table.rows[i].cells[index].innerText.toLowerCase()).indexOf(sample.toLowerCase()) == -1) {
                table.rows[i].setAttribute("style", "display:none")
            }
            else if (sample != '') {
                table.rows[i].setAttribute("style", "display:")
            }
            else {
                table.rows[i].setAttribute("style", "display:")
            }
        }
    }

    table_th.each(function (index) {
        var input = $(this).find('input');
        input.on('input keyup', function (e) {
            // console.log(input.val());
            filter_data(index, String(input.val()))
        })
    })
}