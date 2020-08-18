// check the previous answer if there is previous answer then radio become checked

$(window).on("load", function () {
    $.ajax({
        url: prev_user_answer,
        data: {
            'question_id': question_id,
        },
        success: function (data) {
            var value = data.candidate_answer;
            $('.options').find(':radio[name=optionsRadios]').prop('checked', false);
            if (value != -1) {
                $('.options').find(':radio[name=optionsRadios][value="' + value + '"]').prop('checked', true);
            }
        }
    })
});
$(document).ready(function () {
    $(".status_change").on('click', function () {
        var status = $(this).attr("data-id");
        var load_url = $(this).attr("data-url");
        var option_number = $("input[name='optionsRadios']:checked").val();

        console.log(status + option_number);
        $.ajax({
            url: save_status,
            data: {
                'question_id': question_id,
                'option_number': option_number,
                'status': status
            },
            success: function (data) {
                var value = data.candidate_answer;
                if (value == -2) {
                    window.location.href = data.url;
                }
                window.location.href = load_url;
             //   setTimeout(function() {
             //       window.location.href = load_url;
             //   }, 1000);
            }
        })
    })
});

// save the answer of the question

// $(document).ready(function () {
//     $("input").on('change', function () {
//         var option_number = $("input[name='optionsRadios']:checked").val();
//         $.ajax({
//             url: save_user_answer,
//             data: {
//                 'option_number': option_number,
//                 'question_id': question_id,
//             },
//             success: function (data) {
//                 var value = data.candidate_answer;
//                 if (value == -2) {
//                     window.location.href = data.url;
//                 }
//                 else {
//                     $('.options').find(':radio[name=optionsRadios]').prop('checked', false);
//                     $('.options').find(':radio[name=optionsRadios][value="' + value + '"]').prop('checked', true);
//                 }
//             }
//         })
//     })
// });

