var t = "";
var res = new Object()
var questionCounter = 0; //Tracks question number
  var selections = []; //Array containing user choices
  var quiz = $('#quiz'); //Quiz div object
var questions;
var current_quiz = ""
var username = ""

async  function load_quiz(quiz_name = "") {
  // alert(quiz_name)
    current_quiz = quiz_name;
  var data = new FormData();
                 data.append('quiz_name', quiz_name);
  await  $.ajax({
                     headers: { "X-CSRFToken": t },
                     type: 'POST',
                     url: "load-quiz-info",
                     data: data,
                     processData: false,
                     contentType: false,
                     success: function(json) {
                       //  alert("suc")
                       // current_quiz = json[Object.keys(json)[0]]
                            questions = json
                     },
                     error: function(json) {
                        alert("err")
                     }
                 })
}
(function() {

  // Click handler for the 'next' button
  $('#next').on('click', function (e) {
    e.preventDefault();

    // Suspend click listener during fade animation
    if(quiz.is(':animated')) {
      return false;
    }
    choose();

    // If no user selection, progress is stopped
    if (isNaN(selections[questionCounter])) {
      alert('Please make a selection!');
    } else {
      questionCounter++;
      displayNext();
    }
  });

  // Click handler for the 'prev' button
  $('#prev').on('click', function (e) {
    e.preventDefault();

    if(quiz.is(':animated')) {
      return false;
    }
    choose();
    questionCounter--;
    displayNext();
  });

  // Click handler for the 'Start Over' button
  $('#start').on('click', function (e) {
    e.preventDefault();

    if(quiz.is(':animated')) {
      return false;
    }
    questionCounter = 0;
    selections = [];
    displayNext();
    $('#start').hide();
  });

  $('#show_result').on('click', function (e) {
    console.log("rg");

  });

  // Animates buttons on hover
  $('.button').on('mouseenter', function () {
    $(this).addClass('active');
  });
  $('.button').on('mouseleave', function () {
    $(this).removeClass('active');
  });

  // Reads the user selection and pushes the value to an array
  function choose() {
    selections[questionCounter] = +$('input[name="answer"]:checked').val();
  }

})();
 function createRadios(index) {
    var radioList = $('<ul>');
    var item;
    var input = '';
    for (var i = 0; i < questions[index].choices.length; i++) {
      item = $('<li>');
      input = '<input type="radio" name="answer" value=' + i + ' />';
      input += questions[index].choices[i];
      item.append(input);
      radioList.append(item);
    }
    return radioList;
  }

 function displayScore() {
    var score = $('<p>',{id: 'question'});
    /*for ( i  = 0; i < selections.length; i++)
    {
        alert(selections[i])
    }
    var numCorrect = 0;
    for (var i = 0; i < selections.length; i++) {
      if (selections[i] === questions[i].correctAnswer) {
        numCorrect++;
      }
    }

    score.append('You got ' + numCorrect + ' questions out of ' +
                 questions.length + ' right!!!');*/
    return score;
  }

function createQuestionElement(index) {
    var qElement = $('<div>', {
      id: 'question'
    });
    //alert("hello")
    ///alert(questions.length)
    var header = $('<h2>Питання ' + (index + 1) + '  з  ' + (questions.length) + '</h2>');
   // var header = "";
    qElement.append(header);

    var question = $('<p>').append(questions[index].question);
    qElement.append(question);

    var radioButtons = createRadios(index);
    qElement.append(radioButtons);

    return qElement;
  }


async function displayNext(quiz_name = "") {
     $('#show_result').hide();
    if(quiz_name!= "")
        await load_quiz(quiz_name) ;
   // await alert("fff")
    quiz.fadeOut(function() {
      $('#question').remove();

      if(questionCounter < questions.length){
        //  alert("fff")
        var nextQuestion = createQuestionElement(questionCounter);
        quiz.append(nextQuestion).fadeIn();
        if (!(isNaN(selections[questionCounter]))) {
          $('input[value='+selections[questionCounter]+']').prop('checked', true);
        }

        // Controls display of 'prev' button
        if(questionCounter === 1){
          $('#prev').show();
        } else if(questionCounter === 0){

          $('#prev').hide();
          $('#next').show();
        }
      }else {
        var scoreElem = displayScore();
        quiz.append(scoreElem).fadeIn();
        $('#next').hide();
        $('#prev').hide();
        $('#start').show();
        $('#show_result').show();
        $('#show_result').href = 'statistic/'+username;
        var arr = [current_quiz,username]

        for(i = 0; i < questions.length;i++) {
            arr[i+2] = JSON.stringify({ "question": questions[i]["question"],
                        "choices":  questions[i]["choices"][selections[i]] ,
                        "correctAnswer": questions[i]["correctAnswer"][selections[i]]})
        }
         var data = new FormData();
                 data.append('data', JSON.stringify(arr));
  $.ajax({
                     headers: { "X-CSRFToken": t },
                     type: 'POST',
                     url: "load-test-pass-info",
                     data: data/*{ current_quiz: arr}*/,
                     processData: false,
                     contentType: false,
                     success: function(json) {
                        // alert('TRUE');
                        // alert(json["name"]);
                     },
                     error: function(json) {
                        alert("err");
                       //  alert(json);
                     }
                 })



      }
    });
  }
