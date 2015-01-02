var scan_url="/scan/f56fd125-0515-49ad-bf45-ca8e4c739ef0";
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
