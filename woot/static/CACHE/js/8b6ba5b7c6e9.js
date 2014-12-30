var scan_url="/scan/e03c31c3-5066-4344-b31c-cd6dacd3cea4";
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
