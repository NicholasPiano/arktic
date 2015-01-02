var scan_url="/scan/9f409335-75ab-40c2-9e6c-86226f137658";
var set_delay = 2000;
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
