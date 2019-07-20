$("#updateNameButton").click(updateNameOnclick);
$("#confirmNameButton").click(confirmNameOnclick);

function updateNameOnclick(){
    var teamName = $("#teamName");
    teamName.addClass("hide");
    $("#teamNameEdit").removeClass("hide");
    $("#updateNameButton").addClass("hide");
    $("#confirmNameButton").removeClass("hide");
    }

function confirmNameOnclick(){
    var teamName = $("#teamName");
    var teamNameTextField = $("#teamNameTextField");
    $.ajax({
        url: "/update_team_name",
        dataType: "json",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({"name": teamNameTextField.val()}),
        success: function(data){
            $("#teamName").text(data.team_name);
            $("#teamNameEdit").addClass("hide");
            $("#updateNameButton").removeClass("hide");
            $("#confirmNameButton").addClass("hide");
            teamName.removeClass("hide");
        },
        error: function(jqxhr, textStatus, errorThrown){
            Swal.fire({'text': jqxhr.responseJSON.msg, 'type': 'error'});
        }
    });
}

function switchActiveTeam(inp){
    if (inp.checked){
        $(".future").addClass('hide');
        // activex as otherwise clashes with materialize active class name
        $(".activex").removeClass('hide');
        showingActive = true;
    }
    else{
        $(".future").removeClass('hide');
        $(".activex").addClass('hide');
        showingActive = false;
    }

}