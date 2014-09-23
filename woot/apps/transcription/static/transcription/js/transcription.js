//--CALLBACKS
function action_register_callback (data) { //data is serialized json object

}

function update_transcription_callback (data) {

}

$(document).ready(function() {

  //--SETUP AND BINDINGS
  //set up play variable for play-pause button
  var play = $('li.audio:first audio').attr('id');
  $('#play-pause').attr('play', play);

  //set up utterance buttons
//   $('#panel-'+play).toggle();

  //bind audio player load
  $('audio').on('canplay canplaythrough', function(){
    var play = $(this).attr('id');
    $('#indicator-ok-'+play).css('display','inline-block');
    $('#indicator-loading-'+play).hide();
  });

  //bind audio player end
  $('audio').on('ended', function(){
    Dajaxice.apps.transcription.action_register(action_register_callback, {'job_id':$('#job').attr('job_id'), 'button_id':'audio_ended', 'transcription_id':$('#play-pause').attr('play')});
    //toggle the play-pause button glyphicons if the play variable is the same
    if ($('#play-pause').attr('play') == $(this).attr('id')) {
      $('#play-pause').children('span.glyphicon').toggle();
      $('#play-pause').removeClass('btn-warning').addClass('btn-success');
    }
  });

  //--BUTTONS
  //-id main control buttons
  $('#previous').click(function(){
    Dajaxice.apps.transcription.action_register(action_register_callback, {'job_id':$('#job').attr('job_id'), 'button_id':'previous', 'transcription_id':$('#play-pause').attr('play')});
    //get current play
    var currentPlay = $('#play-pause').attr('play');
    //pause current player and set currentTime=0
    var currentPlayer = document.getElementById(currentPlay);
    if (!currentPlayer.paused) {
      currentPlayer.pause();
      currentPlayer.currentTime=0;
    } else {
      $('#play-pause').children('span.glyphicon').toggle();
    }

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
    Dajaxice.apps.transcription.action_register(action_register_callback, {'job_id':$('#job').attr('job_id'), 'button_id':'replay', 'transcription_id':$('#play-pause').attr('play')});
    var play = $('#play-pause').attr('play');
    var player = document.getElementById(play);
    if (player.paused) {
      $('#play-pause').click();
    } else {
      player.currentTime=0;
    }
  });

  $('#play-pause').click(function(){
    Dajaxice.apps.transcription.action_register(action_register_callback, {'job_id':$('#job').attr('job_id'), 'button_id':'play_pause', 'transcription_id':$('#play-pause').attr('play')});
    //toggle glyphicons
    $(this).children('span.glyphicon').toggle();
    $(this).removeClass('btn-success').addClass('btn-warning');
    //play audio player
    var play = $(this).attr('play');
    var player = document.getElementById(play);

    if (player.paused) {
      player.play();
    } else {
      player.pause();
    }
  });

  $('#next').click(function(){
//     Dajaxice.apps.transcription.action_register(action_register_callback, {'job_id':$('#job').attr('job_id'), 'button_id':'next', 'transcription_id':$('#play-pause').attr('play')});
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

  $('#waveform').click(function(){
    Dajaxice.apps.transcription.action_register(action_register_callback, {'job_id':$('#job').attr('job_id'), 'button_id':'waveform', 'transcription_id':$('#play-pause').attr('play')});
  });

  $('#add-new-word').click(function(){
    Dajaxice.apps.transcription.action_register(action_register_callback, {'job_id':$('#job').attr('job_id'), 'button_id':'add_new_word', 'transcription_id':$('#play-pause').attr('play')});
    //make a new button and add it to the current modified list with copied text from input
    var play = $('#play-pause').attr('play');
    if (play!=='') {
      var text = $('#typeahead').val();
      if (text!='undefined' && text!=='') {
        var active = $('#panel-'+play+' div.modified-panel div.btn-group.modified button.active');
        active.after('<button type="button" class="btn btn-default modified active">' + text + '</button>');
        active.removeClass('active');
        $('#typeahead').blur();
        $('#typeahead').focus();
        $('#typeahead').typeahead('val', '');
      }
      //make tick button not green
      $('#panel-'+play+' div.modified-panel button.tick').addClass('btn-default').removeClass('btn-success');
      $('#indicator-ok-'+play).addClass('btn-default').removeClass('btn-success');
    }
  });

  //-class buttons (general for each transcription object)
  $('button.copy-down').click(function(){
    Dajaxice.apps.transcription.action_register(action_register_callback, {'job_id':$('#job').attr('job_id'), 'button_id':'copy_down', 'transcription_id':$('#play-pause').attr('play')});
    var play = $('#play-pause').attr('play');
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
    Dajaxice.apps.transcription.action_register(action_register_callback, {'job_id':$('#job').attr('job_id'), 'button_id':'add_modified', 'transcription_id':$('#play-pause').attr('play')});
      $('#typeahead').focus();
      $('#typeahead').typeahead('val', '');
  });

  $('div.modified').on('click', 'button.modified', function(){
    Dajaxice.apps.transcription.action_register(action_register_callback, {'job_id':$('#job').attr('job_id'), 'button_id':'modified', 'transcription_id':$('#play-pause').attr('play')});
    //add active class and remove from all others
    $(this).siblings('button.modified').removeClass('active');
    $(this).addClass('active');
    $('#typeahead').focus();
    $('#typeahead').typeahead('val', '');
  });

  $('button.tick').click(function(){
    Dajaxice.apps.transcription.action_register(action_register_callback, {'job_id':$('#job').attr('job_id'), 'button_id':'tick', 'transcription_id':$('#play-pause').attr('play')});
    //send transcription update
    var play = $('#play-pause').attr('play');
    var utterance = '';
    $('#panel-'+play + ' div.modified-panel div.btn-group.modified button.modified').not('button.add-modified').not('button.begin-modified').each(function(){
      utterance += $(this).html() + ' ';
    });
    if (utterance!=='') {
      Dajaxice.apps.transcription.update_transcription(update_transcription_callback, {'job_id':$('#job').attr('job_id'), 'transcription_id':play, 'transcription_utterance':utterance,});
      //toggle green
      $(this).addClass('btn-success').removeClass('btn-default');
      $('#indicator-ok-'+play).addClass('btn-success').removeClass('btn-default');
    }
  });

  $('div.indicator-ok').click(function(){
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
    if([37, 38, 39, 40].indexOf(e.keyCode) > -1) {
        e.preventDefault();
    }
  }, false);

  $(document).keydown(function(e) {
    var play = $('#play-pause').attr('play');
    if (e.ctrlKey && e.keyCode===74) { //ctrl + j
        //previous transcription
        $('#previous').click();
    } else if (e.ctrlKey && e.keyCode===75) { //ctrl + k
        //copy down, tick, next
        var utterance = '';
        $('#panel-'+play + ' div.modified-panel div.btn-group.modified button.modified').not('button.add-modified').not('button.begin-modified').each(function(){
          utterance += $(this).html() + ' ';
        });
        if (utterance=='') {
          $('#panel-'+play+' div.original-panel div.original button.copy-down').click();
          $('#panel-'+play+' div.modified-panel button.tick').click();
          $('#next').click();
        } else {
          $('#panel-'+play+' div.modified-panel button.tick').click();
          $('#next').click();
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
              $('#next').click();
          }
       }
    } else if (e.keyCode === 40) { //down arrow
      if ($('#typeahead').val()=='') {
        $('#next').click();
      }
    } else if (e.keyCode === 16) { //shift (both)
    //   $('#replay').click();
    } else if (e.keyCode === 38) { //up arrow
      if ($('#typeahead').val()=='') {
        $('#previous').click();
      }
    } else if (e.keyCode === 37) { //left arrow
      if ($('#typeahead').val()=='') {
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
        $('#replay').click();
        $('#panel-'+play+' div.modified-panel button.tick').addClass('btn-default').removeClass('btn-success');
        $('#indicator-ok-'+play).addClass('btn-default').removeClass('btn-success');
    } else if (e.keyCode === 39) { //right arrow
      if ($('#typeahead').val()=='') {
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
