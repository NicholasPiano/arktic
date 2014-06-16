$(document).ready(function() {

  //play-pause buttons
  $('button.btn-play-pause').click(function(){
    $(this).children('span.glyphicon').toggle();

    var play = $(this).attr('play');
    var player = document.getElementById(play);

    //if the player is currently playing, pause it.
    if (player.paused) {
      player.play();
    } else {
      player.pause();
    }

    //if the main transcription button has its 'play' attr set to the same as the button, toggle it.
    if ($('#main-play-pause').attr('play')==play) {
      $('#main-play-pause').children('span.glyphicon').toggle();
    }
  });

  //handle audio player stopping
  $('audio').on('ended', function(){
    $(this).siblings('.btn-group').children('button.transcription-play-pause').children('span.glyphicon').toggle();
    //if main transcription button is set to the same id, toggle it.
    if ($('#main-play-pause').attr('play')==$(this).attr('id')) {
      $('#main-play-pause').children('span.glyphicon').toggle();
    }
  });

  //delegate main play-pause button
  $('#main-play-pause').click(function(){
    //toggle
    $(this).children('span.glyphicon').toggle();
    //if attr 'play' is set, play the corresponding audio element.
    var play = $(this).attr('play');
    if (play!='') {
      var player = document.getElementById(play);

      //if the player is currently playing, pause it.
      if (player.paused) {
        player.play();
      } else {
        player.pause();
      }

      //toggle corresponding button
      $('audio#'+play).siblings('.btn-group').children('button.transcription-play-pause').children('span.glyphicon').toggle();
    }
  });

  //transcription-utterance buttons give focus
  $('button.transcription-utterance').click(function(){
    //if another player is playing, stop it.
    var mainPlay = $('#main-play-pause').attr('play');
    if (mainPlay!='') {
      var player = document.getElementById(mainPlay);
      if (!player.paused) {
        player.pause();
        player.currentTime = 0;
        $('#main-play-pause').children('span.glyphicon').toggle();
        $('#button-'+mainPlay).children('span.glyphicon').toggle();
      }
    }

    //if the player associated with this button, is playing, start from the beginning
    var play = $(this).attr('play');
    var currentPlayer = document.getElementById(play);
    if (!currentPlayer.paused) {
      currentPlayer.currentTime = 0;
      $('#main-play-pause').children('span.glyphicon').toggle();
    }

    //highlight and de-highlight others
    $(this).attr('href','');
    $(this).addClass('active');
    $('button.transcription-utterance').not(this).removeAttr('href');
    $('button.transcription-utterance').not(this).removeClass('active');

    //set play attr of main play pause button
    $('#main-play-pause').attr('play',play);

    //make working surface of this id visible and all other invisible
    var ws = $('#ws-'+play);
    ws.show();
    $('ul.control').not(ws).hide();
  });

  //up button
  $('#previous-transcription').click(function(){
    //- find li with same play id as main
    var play = $('#main-play-pause').attr('play');
    var li = $('li.transcription').first();
    if (play!='') {
      li = $('#li-'+play).prev().length ? $('#li-'+play).prev() : $('#li-'+play).first();
    }
    //- click utterance button inside li
//     alert(li.children('div.btn-group').children('button.transcription-utterance').first().attr('id'));
    li.children('div.btn-group').children('button.transcription-utterance').first().click();

    //scroll to li
    $('html, body').stop().animate({
      scrollTop: li.offset().top-65 //height of menu bar
    }, 500);

    //play the player
    $('#main-play-pause').click();
  });

  //down button
  $('#next-transcription').click(function(){
    //- find li with same play id as main
    var play = $('#main-play-pause').attr('play');
    var li = $('li.transcription').first();
    if (play!='') {
      li = $('#li-'+play).next().length ? $('#li-'+play).next() : $('#li-'+play).last();
    }
    //- click utterance button inside li
//     alert(li.children('div.btn-group').children('button.transcription-utterance').first().attr('id'));
    li.children('div.btn-group').children('button.transcription-utterance').first().click();

    //scroll to li
    $('html, body').stop().animate({
      scrollTop: li.offset().top-65 //height of menu bar
    }, 500);

    //play the player
    $('#main-play-pause').click();
  });

  //new word button
  $('#add-new-word').click(function(){
    //make a new button and add it to the current modified list with copied text from input
    var play = $('#main-play-pause').attr('play');
    if (play!='') {
      var text = $('#typeahead').val();
      if (text!='undefined' && text!='') {
        var active = $('ul#ws-'+play+' li.modified div.btn-group.modified button.active');
        active.after('<button type="button" class="btn btn-default modified active">' + text + '</button>');
        active.removeClass('active');
        $('#typeahead').blur();
        $('#typeahead').focus();
        $('#typeahead').typeahead('val', '');
      }
    }
  });

  //initialise tooltips
  $('.has-tooltip').tooltip();

  //add word button - focus typeahead field (maybe unnecessary)
  $('button.modified-add').click(function(){
    $('#typeahead').focus();
    $('#typeahead').typeahead('val', '');
  });

  //copy down button
  $('button.copy-down').click(function(){
    //for each button in the same group, make a new modified button in the correct field.
    var play = $('#main-play-pause').attr('play');
    if (play!='') {
      if ($('ul#ws-'+play+' li.modified div.btn-group.modified button:last').siblings().size() == 0) {
        $('ul#ws-'+play+' li.modified div.btn-group.modified button:last').before('<button type="button" class="btn btn-default modified modified-begin">...</button>');
        $(this).siblings().each(function(){
          $('ul#ws-'+play+' li.modified div.btn-group.modified button:last').before('<button type="button" class="btn btn-default modified">' + $(this).html() + '</button>');
        });
        $('ul#ws-'+play+' li.modified div.btn-group.modified button.modified-add').prev().addClass('active');
      }
    }
  });

  //prevent default actions for arrow keys and space
  window.addEventListener("keydown", function(e) {
    // space and arrow keys
    if([37, 38, 39, 40].indexOf(e.keyCode) > -1) {
        e.preventDefault();
    }
  }, false);

  //shortcuts
  $(document).keydown(function(e) {
    var play = $('#main-play-pause').attr('play');
    if(e.keyCode === 13) { //enter
      //controlling word copying
      if ($('#typeahead').is(':focus') && $('#typeahead').val()!='') {
        $('#add-new-word').click();
      } else {
        $('ul#ws-'+play+' li.original div.btn-group button.copy-down').click();
      }
    } else if (e.keyCode === 40) { //down arrow
      if ($('#typeahead').val()=='') {
        $('#next-transcription').click();
      }
    } else if (e.keyCode === 38) { //up arrow
      if ($('#typeahead').val()=='') {
        $('#previous-transcription').click();
      }
    } else if (e.keyCode === 37) { //left arrow
      if ($('#typeahead').val()=='') {
        //if no button is active, go to last word button
        //else go to button to the left of active one
        if ($('ul#ws-'+play+' li.modified div.btn-group button.modified.active').prev().length) {
          $('ul#ws-'+play+' li.modified div.btn-group button.modified.active').removeClass('active').prev().addClass('active');
          //focus typeahead
          $('#typeahead').focus();
          $('#typeahead').typeahead('val', '');
        }
      }
    } else if (e.keyCode === 39) { //right arrow
      if ($('#typeahead').val()=='') {
        //if no button is active, go to first word button
        //else go to button to the right of active one
        if ($('ul#ws-'+play+' li.modified div.btn-group button.modified.active').next().not('button.modified-add').length) {
          $('ul#ws-'+play+' li.modified div.btn-group button.modified.active').removeClass('active').next().not('button.modified-add').addClass('active');
          //focus typeahead
          $('#typeahead').focus();
          $('#typeahead').typeahead('val', '');
        }
      }
    } else if (e.keyCode === 32) { //space bar
//       if (!$('#typeahead').is(':focus')) {
//         $('#typeahead').focus();
//         $('#typeahead').typeahead('val', '');
//       }
    } else if (e.keyCode === 8) {
      if ($('#typeahead').val()=='') {
        //delete active button and make the button to the left active
        //if the button is the left most, make the button to thr right active
        var active = $('ul#ws-'+play+' li.modified div.btn-group button.modified.active');
        if (active.prev().length) {
          active.prev().addClass('active');
        } else {
          active.next().not('button.modified-add').addClass('active');
        }
        active.not('button.modified-begin').remove();
      }
    }
  });

  //set up audio and working surface
  $('#next-transcription').click();

});
