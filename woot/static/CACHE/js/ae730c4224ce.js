var scan_url="/scan/5cc76a1b-7bd1-4d99-a06f-9407c6b8c8a0";
var set_delay = 1000;
var callout = function () {
      $.ajax({
        url:scan_url
      })
      .done(function (response) {
        $("#client-list").html(response)
        $("#client-list").attr("status", $("#client-list").children('a').first().attr("status"))
      })
      .always(function () {
        if ($("#client-list").attr('status')=="loading") {
          setTimeout(callout, set_delay);
        }
      });
    };

// initial call
callout();
