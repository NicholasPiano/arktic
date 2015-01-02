var set_delay = 2000,
    callout = function () {
        $.ajax({
            url:"/scan/"
        })
        .done(function (response) {
            $('#load').text($('#load').text() + response)
            if (response==' Done.') {
                $('#load').addClass('done')
            }
        })
        .always(function () {
            if (!$('#load').hasClass('done')) {
                setTimeout(callout, set_delay);
            }
        });
    };

// initial call
// callout();
