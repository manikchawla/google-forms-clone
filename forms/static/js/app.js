
var addOption = function() {
    var html = "<div class=\"answer-type\">";
    html += "<input type=\"text\" class=\"form-control option\" name=\"option\" placeholder=\"Enter option text\">";
    html += "<button class=\"btn btn-danger delete-option\">Delete Option</button>";
    html += "</div>";
    return html;
}

var formSubmit = function() {
    var questionsObj = [];
    var questions = $('.question-card');
    questions.each(function(question) {
        var questObj = {};
        var question_text = $(this).find('.question-text').val();
        if (question_text.trim().length > 0) {
            questObj['text'] = question_text;
            questObj['type'] = $(this).find('.question-type').val();
            if (questObj['type'] == 'mcq_one' || questObj['type'] == 'mcq_many') {
                var options = $(this).find('.option');
                var options_array = [];
                options.each(function(option) {
                    var option_text = $(this).val();
                    if (option_text.trim().length > 0) {
                        options_array.push(option_text);
                    }
                });
                questObj['options'] = options_array;
            }
            questionsObj.push(questObj);
        }
    });
    return questionsObj;
}

var addQuestion = function() {
    var new_question = $('.question-card').first().clone();
    new_question.find('.question-text').val('');
    new_question.find('.answer-type').remove();
    var default_answer_type = "<div class=\"answer-type\">";
    // default_answer_type += "<input type=\"text\" class=\"form-control\" placeholder=\"Text answer\">";
    default_answer_type += "</div>";
    new_question.find('.answer').append(default_answer_type);
    // new_question.attr('id', 'question-card-' + (++question_card_id));
    var delete_btn = "<button class=\"btn btn-danger delete-question\">Delete</button>";
    new_question.append(delete_btn);
    $('.card-holder').append(new_question);
};

var duplicateQuestion = function() {
    var original_question = $(this).parents('.question-card');
    var duplicate_question = original_question.clone();
    var question_type_value = original_question.find('.question-type').val();
    duplicate_question.find('.question-type').val(question_type_value);
    if (original_question.is(':first-child')) {
        var delete_btn = "<button class=\"btn btn-danger delete-question\">Delete</button>";
        duplicate_question.append(delete_btn);
    }
    original_question.after(duplicate_question);
};


var changeQuestionType = function(type) {
    var html = "";
    switch(type) {
        case 'text':
            // html = "<input type=\"text\" class=\"form-control answer-type\" placeholder=\"Text answer\">";
            break;
        case 'mcq_one':
        case 'mcq_many':
            html = "<div class=\"answer-type\">";
            html += "<input type=\"text\" class=\"form-control option\" name=\"option\" placeholder=\"Option 1\" value=\"Option 1\">";
            html += "</div>";
            html += "<button class=\"btn btn-primary add-option\">Add Option</button>";
            break;
        case 'binary':
            html = "<div class=\"form-check answer-type\">"
            html += "<label class=\"form-check-label\">";
            html += "<input class=\"form-check-input\" type=\"radio\" value=\"yes\" disabled>";
            html += "<span class=\"option-text\">Yes</span>";
            html += "</label>";
            html += "</div>";
            html += "<div class=\"form-check answer-type\">"
            html += "<label class=\"form-check-label\">";
            html += "<input class=\"form-check-input\" type=\"radio\" value=\"no\" disabled>";
            html += "<span class=\"option-text\">No</span>";
            html += "</label>";
            html += "</div>";
            break;
        default:;   
    }
    return html;
};

var ajaxSubmit = function(data) {
    var csrf_token = $("[name='csrfmiddlewaretoken']").val();
    // ajax form submit
    $.ajax({
        url: 'form_create/',
        type: 'POST',
        headers: {'X-CSRFToken': csrf_token},
        data: data,
        dataType: 'json',
        timeout: 5000,
        success: function(response) {
            var html = "<span class=\"message\">" + response['result'] + "</span>"
            $('.messages').append(html);
            $('.message').delay(5000).fadeOut();
        }
    });
};

$(document).ready(function() {

    // add new question handler
    $('.create-form').on('click', '.add-question', function(e) {
        e.preventDefault();
        addQuestion();
    });

    // duplicate question handler
    $('.create-form').on('click', '.duplicate-question', function(e) {
        e.preventDefault();
        duplicateQuestion.call(this);
    })

    // delete question handler
    $('.create-form').on('click', '.delete-question', function() {
        $(this).parents('.card').remove();
    });

    // change question type handler
    $('.create-form').on('change', '.question-type', function() {
        var html = changeQuestionType($(this).val());
        $(this).parents('.card-block').find('.answer-type').remove();
        $(this).parents('.card-block').find('.answer').append(html);
    });

    // add option for mcq questions handler
    $('.create-form').on('click', '.add-option',function(e) {
        e.preventDefault();
        var option = addOption();
        // $(this).parents('.answer').append(option);
        $(this).parents('.answer').find('.add-option').before(option);
    });

    $('.create-form').on('click', '.delete-option', function(e) {
        e.preventDefault();
        console.log(this);
        $(this).parents('.answer-type').remove();
    });

    $(document).on('submit', '.create-form', function(e) {
        e.preventDefault();
        var requestObj = {};
        requestObj['questions'] = formSubmit();
        requestObj['form_title'] = $('.form-title').val();
        requestObj['form_description'] = $('.form-description').val(); 
        console.log(requestObj);
        requestJson = JSON.stringify(requestObj);
        ajaxSubmit(requestJson);  

    });      

});
