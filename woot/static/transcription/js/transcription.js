$(document).ready(function() {

  var numchars = ["zero","one","two","three","four","five","six","seven","eight","nine"];

  //--SETUP AND BINDINGS
  //set up play variable for play-pause button
  var play = $('li.audio:first audio').attr('id');
  $('#play-pause').attr('play', play);

  //bind audio player load
  $('audio').on('canplay canplaythrough', function(){
    var play = $(this).attr('id');
    $('#indicator-ok-'+play).removeClass('ninja');
    $('#indicator-loading-'+play).hide();
  });

  //bind audio player end
  $('audio').on('ended', function(){
    var play = $(this).attr('id');
//     action_register(play, 'ended audio', 0);
    //toggle the play-pause button glyphicons if the play variable is the same
    if ($('#play-pause').attr('play') == $(this).attr('id')) {
      $('#play-pause').children('span.glyphicon').toggle();
      $('#play-pause').removeClass('btn-warning').addClass('btn-success');
    }
  });

  //--BUTTONS
  //-id main control buttons
  $('#previous').click(function(){
    //get current play
    var currentPlay = $('#play-pause').attr('play');
    //pause current player and set currentTime=0
    var currentPlayer = document.getElementById(currentPlay);
    if (!currentPlayer.paused) {
      $('#now-'+currentPlay).stop();
      currentPlayer.pause();
      currentPlayer.currentTime=0;
    } else {
      $('#play-pause').children('span.glyphicon').toggle();
      currentPlayer.currentTime=0;
    }
    $('#now-'+currentPlay).css('left','0px');

    //get next id
    var prevPlay = $('#li-'+currentPlay).prev().length ? $('#li-'+currentPlay).prev().children('audio').attr('id') : $('#li-'+currentPlay).first().children('audio').attr('id');
    var prevPlayer = document.getElementById(prevPlay);

    //set play-pause button play variable
    $('#play-pause').attr('play', prevPlay);
    //toggle and click button
    $('#play-pause').children('span.glyphicon').toggle();
    $('#play-pause').click();

    //counter label
    var counter = $('#li-'+prevPlay).attr('index');
    $('#counter span').html(counter);

    //show utterance and hide others
    $('div.transcription').css('display','none');
    $('#panel-'+prevPlay).css('display','block');

    //indicator highlight
    //indicator highlight
    $('div.indicator.active-indicator').removeClass('active-indicator');
    $('#indicator-ok-'+prevPlay).addClass('active-indicator');
  });

  $('#replay').click(function(){
    var play = $('#play-pause').attr('play');
    var player = document.getElementById(play);
    action_register(play, 'replay', player.currentTime);
    $('#now-'+play).css('left','0px');
    $('#now-'+play).stop();
    if (player.paused) {
      $('#play-pause').click();
    } else {
      player.currentTime=0;
      var duration = parseFloat($('#wave-'+play).attr('length'))*1000;
      $('#now-'+play).animate({left: "200px"}, duration, "linear", function() {$('#now-'+play).css('left','0px');});
    }

  });

  $('#back').click(function(){
    var play = $('#play-pause').attr('play');
    var player = document.getElementById(play);
    action_register(play, 'replay', player.currentTime);
    $('#now-'+play).stop();
    if (player.paused) {
      $('#play-pause').click();
    } else {
      if (player.currentTime >= 2) {
        player.currentTime=player.currentTime-2;
      } else {
        player.currentTime=0;
      }
      var duration = parseFloat($('#wave-'+play).attr('length'))*1000;
      var position = (player.currentTime*200000/duration) + "px";
      $('#now-'+play).css('left',position);
      $('#now-'+play).animate({left: "200px"}, duration-player.currentTime*1000, "linear", function() {$('#now-'+play).css('left','0px');});
    }
  });

  $('#play-pause').click(function(){
    //toggle glyphicons
    $(this).children('span.glyphicon').toggle();
    $(this).removeClass('btn-success').addClass('btn-warning');
    //play audio player
    var play = $(this).attr('play');
    var player = document.getElementById(play);
//     action_register(play, 'play', player.currentTime);

    if (player.paused) {
      player.play();
      var duration = parseFloat($('#wave-'+play).attr('length'))*1000;
      $('#now-'+play).animate({left: "200px"}, duration-player.currentTime*1000, "linear", function() {$('#now-'+play).css('left','0px');});
    } else {
      player.pause();
      $('#now-'+play).stop();
    }
  });

  $('#next').click(function(){
    //get current play
    var currentPlay = $('#play-pause').attr('play');
    $('#panel-'+currentPlay+' div.modified-panel div.tick button.tick').click();
    $('#now-'+currentPlay).stop();
    $('#now-'+currentPlay).css('left','0px');
    //pause current player and set currentTime=0
    var currentPlayer = document.getElementById(currentPlay);
    if (!currentPlayer.paused) {
      currentPlayer.pause();
      currentPlayer.currentTime=0;
    } else {
      $('#play-pause').children('span.glyphicon').toggle();
      currentPlayer.currentTime=0;
    }

    //get next id
    var nextPlay = $('#li-'+currentPlay).next().length ? $('#li-'+currentPlay).next().children('audio').attr('id') : $('#li-'+currentPlay).last().children('audio').attr('id');

    //set play-pause button play variable
    $('#play-pause').attr('play', nextPlay);
    //toggle and click button
    $('#play-pause').children('span.glyphicon').toggle();
    $('#play-pause').click();

    //counter label
    var counter = $('#li-'+nextPlay).attr('index');
    $('#counter span').html(counter);

    //show utterance and hide others
    $('div.transcription').css('display','none');
    $('#panel-'+nextPlay).css('display','block');

    //indicator highlight
    $('div.indicator.active-indicator').removeClass('active-indicator');
    $('#indicator-ok-'+nextPlay).addClass('active-indicator');
  });

  $('#add-new-word').click(function(){
    //make a new button and add it to the current modified list with copied text from input
    var play = $('#play-pause').attr('play');
    var player = document.getElementById(play);
//     action_register(play, 'add new word', player.currentTime);
    if (play!=='') {
      var text = $('#typeahead').val();
      if (text!='undefined' && text!=='') {
        var active = $('#panel-'+play+' div.modified-panel div.btn-group.modified button.active');
        if (isNaN(text)) {
          active.after('<button type="button" class="btn btn-default modified active">' + text + '</button>');
          active.removeClass('active');
        } else {
          var nums = text.split("");
          for (i=0;i<nums.length;i++) {
            var newtext = numchars[parseInt(nums[i])];
            active.after('<button type="button" class="btn btn-default modified active">' + newtext + '</button>');
            active.removeClass('active');
            active = $('#panel-'+play+' div.modified-panel div.btn-group.modified button.active');
          }
        }
        $('#typeahead').blur();
        $('#typeahead').focus();
        $('#typeahead').typeahead('val', '');
      }
      //make tick button not green
      $('#panel-'+play+' div.modified-panel button.tick').addClass('btn-default').removeClass('btn-success');
      $('#indicator-ok-'+play).addClass('btn-default').removeClass('btn-success');

      //hide new job button
      $('#new-job-button').addClass('ninja');
    }
  });

  $('#common').click(function(){
    var play = $('#play-pause').attr('play');
    if (play!=='') {
      var text = $('#typeahead').val();
      if (text!='undefined' && text!=='') {
        $('#typeahead').blur();
        $('#typeahead').focus();
        $('#typeahead').typeahead('val', '');
        add_word(play, text);
        words.push(text);
      }
    }
  });

  $('#slide-out-panel').click(function(){
    if ($(this).css('right')==='-385px') {
      $(this).animate({
        right: '0px',
      }, 200);
    } else {
      $(this).animate({
        right: '-385px',
      }, 200);
    }
  });

  $('#shortcuts-panel').click(function(){
    if ($(this).css('right')==='-385px') {
      $(this).animate({
        right: '0px',
      }, 200);
    } else {
      $(this).animate({
        right: '-385px',
      }, 200);
    }
  });

  $('#new-job-button').click(function(){window.location='/new/'});

  //-class buttons (general for each transcription object)
  $('button.copy-down').click(function(){
    var play = $('#play-pause').attr('play');
    var player = document.getElementById(play);
//     action_register(play, 'copy down', player.currentTime);
    if ($('#panel-'+play+' div.modified-panel div.modified').children().size() == 2) { //only ... should be there
      var utterance = $('#panel-'+play+' div.original-panel div.original button.original-utterance').html();
      if (typeof utterance === "undefined") {
        $('#panel-'+play+' div.modified-panel div.modified button.add-modified').click();
      } else {
        $('#panel-'+play+' div.modified-panel div.modified button.begin-modified').removeClass('active');
        var word_array = utterance.split(" ");
        word_array.forEach(function(word){
          $('#panel-'+play+' div.modified-panel div.modified button.add-modified').before('<button type="button" class="btn btn-default modified">' + word + '</button>');
        });
        //remove class 'active'
        $('#panel-'+play+' div.modified-panel div.modified button.add-modified').prev().addClass('active');
      }
    }

  });

  $('button.add-modified').click(function(){
      $('#typeahead').focus();
      $('#typeahead').typeahead('val', '');
  });

  $('div.modified').on('click', 'button.modified', function(){
    //add active class and remove from all others
    $(this).siblings('button.modified').removeClass('active');
    $(this).addClass('active');
    $('#typeahead').focus();
    $('#typeahead').typeahead('val', '');
  });

  $('button.tick').click(function(){
    //send transcription update
    var play = $('#play-pause').attr('play');
    var player = document.getElementById(play);
    action_register(play, 'tick', player.currentTime);
    var utterance = '';
    $('#panel-'+play + ' div.modified-panel div.btn-group.modified button.modified').not('button.add-modified').not('button.begin-modified').each(function(){
      utterance += $(this).html() + ' ';
    });
    if (utterance!=='') {
      //toggle green
      $(this).addClass('btn-success').removeClass('btn-default');
      $('#indicator-ok-'+play).addClass('btn-success').removeClass('btn-default');
    }
  });

  $('div.indicator-ok').not('#new-job-button').click(function(){
    //get current play
    var currentPlay = $('#play-pause').attr('play');
    $('#panel-'+currentPlay+' div.modified-panel div.tick button.tick').click();
    //pause current player and set currentTime=0
    var currentPlayer = document.getElementById(currentPlay);
    if (!currentPlayer.paused) {
      currentPlayer.pause();
      currentPlayer.currentTime=0;
    } else {
      $('#play-pause').children('span.glyphicon').toggle();
    }

    //get next id
    var nextPlay = $(this).attr('play');

    //set play-pause button play variable
    $('#play-pause').attr('play', nextPlay);
    //toggle and click button
    $('#play-pause').children('span.glyphicon').toggle();
    $('#play-pause').click();

    //counter label
    var counter = $('#li-'+nextPlay).attr('index');
    $('#counter span').html(counter);

    //show utterance and hide others
    $('div.transcription').css('display','none');
    $('#panel-'+nextPlay).css('display','block');

    //switch to active
    $('div.indicator.active-indicator').removeClass('active-indicator');
    $(this).addClass('active-indicator');
  });

  //--KEYBOARD SHORTCUTS
  //prevent default actions for arrow keys and space
  window.addEventListener("keydown", function(e) {
    // space and arrow keys
    if([38, 40].indexOf(e.keyCode) > -1) {
        e.preventDefault();
    }
  }, false);

  $(document).keyup(function(e) {
    if (e.keyCode===16) { //shift (both)
      // $('#shortcuts-panel').click();
    }
  });

  $(document).keydown(function(e) {
    var play = $('#play-pause').attr('play');
    if (e.ctrlKey && e.keyCode===74) { //ctrl + j
        //previous transcription
        $('#previous').click();
        $('#typeahead').focus();
        $('#panel-'+play+' div.modified-panel button.tick').addClass('btn-default').removeClass('btn-success');
        $('#indicator-ok-'+play).addClass('btn-default').removeClass('btn-success');
    } else if (e.ctrlKey && e.keyCode===75) { //ctrl + k
        //copy down, tick, next
        var utterance = '';
        $('#panel-'+play + ' div.modified-panel div.btn-group.modified button.modified').not('button.add-modified').not('button.begin-modified').each(function(){
          utterance += $(this).html() + ' ';
        });
        if (utterance=='') {
          $('#panel-'+play+' div.original-panel div.original button.copy-down').click();
        }
        $('#panel-'+play+' div.modified-panel button.tick').click();
        if ($('#indicators div.btn-success.indicator-ok').length === number_of_transcriptions) { //all transcriptions are ticked
          //make "next job button" visible
          if ($('#new-job-button').hasClass('ninja')) {
            $('#new-job-button').removeClass('ninja');
          } else {
            $('#new-job-button').click();
          }
        } else {
          $('#next').click();
        }
    } else if (e.ctrlKey && e.keyCode===13) { //ctrl + enter
      //I see this a lot
      if ($('#typeahead').is(':focus') && $('#typeahead').val()!=='') {
        $('#common').click();
      }
    } else if (e.keyCode === 13) { //enter
        //controlling word copying
        if ($('#typeahead').is(':focus') && $('#typeahead').val()!=='') {
          $('#add-new-word').click();
        } else {
          var utterance = '';
          $('#panel-'+play + ' div.modified-panel div.btn-group.modified button.modified').not('button.add-modified').not('button.begin-modified').each(function(){
            utterance += $(this).html() + ' ';
          });
          if (utterance=='') {
            $('#panel-'+play+' div.original-panel div.original button.copy-down').click();
          } else {
            $('#panel-'+play+' div.modified-panel button.tick').click();
            if ($('#indicators div.btn-success.indicator-ok').length === number_of_transcriptions) { //all transcriptions are ticked
              //make "next job button" visible
              if ($('#new-job-button').hasClass('ninja')) {
                $('#new-job-button').removeClass('ninja');
              } else {
                $('#new-job-button').click();
              }
            } else {
              $('#next').click();
            }
          }
       }
    } else if (e.ctrlKey && e.keyCode === 32) { //ctrl + space
      $('#slide-out-panel').click();
    } else if (e.keyCode === 40) { //down arrow
      if ($('#typeahead').val()=='') {
        $('#next').click();
      }
    } else if (e.shiftKey) { //shift (both)
      // $('#typeahead').blur();

      //All letter combinations
      var text = '';
      if (e.keyCode === 72) { // H
        e.preventDefault()
        text = '[hesitation]';
      } else if (e.keyCode === 66) { //B
        e.preventDefault()
        text = '[breath noise]';
      } else if (e.keyCode === 68) {
        e.preventDefault()
        text = '[dtmf]';
      } else if (e.keyCode === 70) {
        e.preventDefault()
        text = '[fragment]';
      } else if (e.keyCode === 65) {
        e.preventDefault()
        text = '[hangup]';
      } else if (e.keyCode === 77) {
        e.preventDefault()
        text = '[mispronunciation]';
      } else if (e.keyCode === 78) {
        e.preventDefault()
        text = '[noise]';
      } else if (e.keyCode === 80) {
        e.preventDefault()
        text = '[pause]';
      } else if (e.keyCode === 83) {
        e.preventDefault()
        text = '[side speech]';
      } else if (e.keyCode === 85) {
        e.preventDefault()
        text = '[unintelligible]';
      } else if (e.keyCode === 90) {
        e.preventDefault()
        text = '[background noise]';
      } else if (e.keyCode === 67) {
        e.preventDefault()
        text = '[bad audio]';
      } else if (e.keyCode === 69) {
        e.preventDefault()
        text = '[english]';
      } else if (e.keyCode === 79) {
        e.preventDefault()
        text = '[no speech]';
      } else if (e.keyCode === 86) {
        e.preventDefault()
        text = '[non native]';
      } else if (e.keyCode === 82) {
        e.preventDefault()
        text = '[spanish]';
      } else {
        //make shortcut panel slide out
        // $('#shortcuts-panel').click();
      }

      var play = $('#play-pause').attr('play');
      if (play!=='' && text!=='undefined' && text!=='') {
          var active = $('#panel-'+play+' div.modified-panel div.btn-group.modified button.active');
          active.after('<button type="button" class="btn btn-default modified active">' + text + '</button>');
          active.removeClass('active');
      }

    } else if (e.keyCode === 38) { //up arrow
      if ($('#typeahead').val()=='') {
        $('#previous').click();
      }
    } else if (e.keyCode === 37) { //left arrow
      if ($('#typeahead').val()==='') {
        //get active button in group
        var active = $('#panel-'+play+' div.modified-panel div.modified button.modified.active');
        //make button to the left active, if it exists
        if (active.prev().length) {
          active.prev().click();
        }
      }
    } else if (e.keyCode === 9) { //tab
        e.preventDefault()
        $('#typeahead').focus();
        $('#back').click();
        $('#panel-'+play+' div.modified-panel button.tick').addClass('btn-default').removeClass('btn-success');
        $('#indicator-ok-'+play).addClass('btn-default').removeClass('btn-success');

        //hide new job button
        $('#new-job-button').addClass('ninja');
    } else if (e.keyCode === 39) { //right arrow
      if ($('#typeahead').val()==='') {
        //get active button in group
        var active = $('#panel-'+play+' div.modified-panel div.modified button.modified.active');
        //make button to the right active, if it isn't add-modified
        active.next().not('button.add-modified').click();
      }
    } else if (e.keyCode === 8) { //backspace
      if ($('#typeahead').val()=='') {
        e.preventDefault();
        //delete active button and make the button to the left active
        //if the button is the left most, make the button to thr right active
        var active = $('#panel-'+play+' div.modified-panel div.modified button.modified.active');
        if (active.prev().length) {
          active.prev().addClass('active');
        } else {
          active.next().not('button.add-modified').addClass('active');
        }
        active.not('button.begin-modified').remove();
        //make tick button not green
        $('#panel-'+play+' div.modified-panel button.tick').addClass('btn-default').removeClass('btn-success');
        $('#indicator-ok-'+play).addClass('btn-default').removeClass('btn-success');
      }
    }
  });

});
