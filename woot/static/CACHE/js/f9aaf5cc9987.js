var scan_url="/scan/7c5b4abc-9d63-4354-8790-fb84729f9370";
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
