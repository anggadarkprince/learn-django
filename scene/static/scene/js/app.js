$(document).ready(function () {

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

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


    var likerStorageKey = 'scenary-liker';
    var localLikerData = localStorage.getItem(likerStorageKey);
    var likeHistory = localLikerData == null ? [] : JSON.parse(localLikerData)

    function checkHistory(data, key) {
        var isExist = false;
        for (var i = 0; i < data.length; i++) {
            if (key == data[i]) {
                isExist = true;
                break;
            }
        }
        return isExist;
    }

    $('.like-photo').on('click', function (e) {
        e.preventDefault();
        $(this).addClass('text-danger').removeClass('text-muted').addClass('disabled');

        var photoId = $(this).data('photo-id');
        var likeTotal = $(this).find('.like-total');
        likeTotal.text(parseInt(likeTotal.text()) + 1);

        if (!checkHistory(likeHistory, photoId)) {
            $.ajax({
                url: $(this).attr('href'),
                method: 'post',
                dataType: 'json',
                success: function (data) {
                    if (data.status == 'success') {
                        likeHistory.push(photoId);
                        localStorage.setItem(likerStorageKey, JSON.stringify(likeHistory));
                    } else {
                        alert(data.message);
                    }
                },
                error: function (data) {
                    console.log(data.message);
                    debugger;
                }
            });
        }
    });

    $('.like-photo').each(function () {
        var photoId = $(this).data('photo-id');
        if (checkHistory(likeHistory, photoId)) {
            $(this).addClass('text-danger').removeClass('text-muted').addClass('disabled');
        }
    });
});