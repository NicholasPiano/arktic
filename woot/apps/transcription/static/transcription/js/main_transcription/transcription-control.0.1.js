//--CALLBACKS
function action_register_callback (data) { //data is serialized json object

}

function update_transcription_callback (data) {

}

$(document).ready(function() {

  //--SETUP AND BINDINGS
  //set up play variable for play-pause button
  var play = $('li.audio:first audio').attr('id')
  $('#play-pause').attr('play', play);

  //set up utterance buttons
//   $('#panel-'+play).toggle();

  //bind audio player end
  $('audio').on('ended', function(){
    //toggle the play-pause button glyphicons if the play variable is the same
    if ($('#play-pause').attr('play') == $(this).attr('id')) {
      $('#play-pause').children('span.glyphicon').toggle();
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
  });

  $('#replay').click(function(){
    var play = $('#play-pause').attr('play');
    var player = document.getElementById(play);
    player.currentTime=0;
  });

  $('#play-pause').click(function(){
    //toggle glyphicons
    $(this).children('span.glyphicon').toggle();
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
  });

  $('#waveform').click(function(){
    Dajaxice.apps.transcription.action_register(action_register_callback, {'job_id':$('#job').attr('job_id'), 'button_id':'waveform', 'transcription_id':$('#play-pause').attr('play')});
  });

  $('#add-new-word').click(function(){
    //make a new button and add it to the current modified list with copied text from input
    var play = $('#play-pause').attr('play');
    if (play!='') {
      var text = $('#typeahead').val();
      if (text!='undefined' && text!='') {
        var active = $('#panel-'+play+' div.modified-panel div.btn-group.modified button.active');
        active.after('<button type="button" class="btn btn-default modified active">' + text + '</button>');
        active.removeClass('active');
        $('#typeahead').blur();
        $('#typeahead').focus();
        $('#typeahead').typeahead('val', '');
      }
    }
  });

  //-class buttons (general for each transcription object)
  $('button.copy-down').click(function(){

  });

  $('button.add-modified').click(function(){

  });

  $('button.modified').click(function(){

  });

  //--KEYBOARD SHORTCUTS

});
