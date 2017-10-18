//buyBtn.click({form: form}, tradeOnclick);

var draftOnclick = function draftOnclick(event){
    var form = $("#draftForm");
    var allow_dupes = form.find("input[name=allowDuplicates]")[0].checked;
    var use_max = form.find("input[name=useMax]")[0].checked;
    var use_rnn = form.find("input[name=useRnn]")[0].checked;
    var pickbans = [];
    for (var i=0; i<20; i++){
        var hero = $("input[name=pickban" + i + "]").val();
        if (hero == "Ban" || hero == "Pick"){
            break;
        }
        pickbans.push(hero);
    }
    formData = {
        "pickbans": pickbans,
        "use_max": use_max,
        "allow_dupes": allow_dupes,
        "use_rnn": use_rnn
    };
    $.ajax({
        url: "/neuralnet_post",
        type: "POST",
        data: JSON.stringify(formData),
        contentType: 'application/json',
        success: function(data){
            var success = data.success,
            pickbans = data.pickbans,
            message = data.message;
            if (success){
                sweetAlert(message);
                for (var i=0; i<pickbans.length; i++){
                console.log(pickbans[i]);
                console.log($("input[name=pickban" + i + "]"))
                    $("input[name=pickban" + i + "]")[0].value = pickbans[i];
                }
            }
            else{
                sweetAlert(message);
            }
        },
        failure: function(data){
            sweetAlert("Something went wrong. oops!");
        }
    });
}

var clearOnclick = function clearOnclick(){
	$("input[name^=pickban]").each(function(){this.value = "";});
}
$("#draftBtn").click(draftOnclick);
$("#clearBtn").click(clearOnclick);
