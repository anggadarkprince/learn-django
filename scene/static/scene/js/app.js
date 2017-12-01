$(document).ready(function () {
    $('.custom-file-input').on('change', function () {
        var fileName = $(this).val();
        if (fileName !== '') {
            fileName = fileName.split('\\').pop();
        }
        $(this).next('.custom-file-control').addClass('selected').html(fileName);
    });

    $('.date-picker').datepicker({
        autoclose: true
    });
});