$(".leagueLink").click(openLeagueSection);

function openLeagueSection(event){
    var link = $(event.currentTarget);
    var dataId = link.attr("data-id");
    $(".leagueSection").addClass("hide");
    $("#leagueContainer" + dataId).removeClass("hide");
}

// Initialise form values
document.querySelectorAll('.updateForm').forEach(function(form) {
    var leagueId = form.dataset.id;
    var url = apiBaseUrl + "leagues/" + leagueId + "?";
    $.ajax({url: url,
        dataType: "json",
        type: "GET",
        success: function(data){
        if (data.system == "draft"){
           form.querySelector("input[name='name']").value = data.name;
           form.querySelector("input[name='start']").value = data.draftStart.replace("T", " ").split(".", 1)[0];
           form.querySelector("input[name='nextDeadline']").value = data.nextDraftDeadline.replace("T", " ").split(".", 1)[0];
           form.querySelector("input[name='timer']").value = data.choiceTimer;
           }
        }
    })
});

$('.updateForm').on('submit', updateForm);

function updateForm(event){
    console.log(event)
    event.preventDefault();
    var form = event.currentTarget;
    var url = apiBaseUrl + "leagues/" + form.querySelector("input[name='league_id']").value + "?apiKey=" + apiKey;
    var data = {'league': {'leagueName': form.querySelector("input[name='name']").value},
                'draft': {'draftStart': form.querySelector("input[name='start']").value,
                 'nextDraftDeadline': form.querySelector("input[name='nextDeadline']").value,
                 'choiceTimer': parseInt(form.querySelector("input[name='timer']").value)
                 }
        };
    $.ajax({
        url: url,
        dataType: "json",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(data),
        success: function(data){
            Swal.fire({
             title: "Yea boi!",
              type: "success"
            })
        },
        error: function(jqxhr, textStatus, errorThrown){
            Swal.fire(jqxhr.responseText, '', 'error');
        }
    });
}

$('#leagueFormNew').on('submit', newForm);


function newForm(event){
    console.log(event)
    event.preventDefault();
    var form = event.currentTarget;
    var url = "/create_league_proxy";
    var data = {'name': form.querySelector("input[name='name']").value,
                'draftStart': form.querySelector("input[name='start']").value,
                 'choiceTimer': parseInt(form.querySelector("input[name='timer']").value)
        };
    $.ajax({
        url: url,
        dataType: "json",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(data),
        success: function(data){
            Swal.fire({
             title: "Yea boi!",
              type: "success"
            }).then(function(){window.location.reload(false);})
            // Easier to just reload page, than redraw forms
        },
        error: function(jqxhr, textStatus, errorThrown){
            Swal.fire(jqxhr.responseText, '', 'error');
        }
    });
}