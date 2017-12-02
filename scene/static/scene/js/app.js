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

    var modalConfirmArchive = $('#modal-confirm-archive');
    modalConfirmArchive.find('[type=submit]').on('click', function () {
        $(this).attr('disabled', true);
    });
    $('.move-to-archive').on('click', function (e) {
        e.preventDefault();

        var archiveUrl = $(this).attr('href');
        var photoTitle = $(this).data('photo-title');

        modalConfirmArchive.find('form').attr('action', archiveUrl);
        modalConfirmArchive.find('#photo-title').text(photoTitle);
        modalConfirmArchive.modal({
            backdrop: 'static',
            keyboard: false
        });
    });
});