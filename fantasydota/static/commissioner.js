var leaguesToUsers = new Map();
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
               form.querySelector("input[name=manualDraftBtn]").checked = data.manualDraft;
               // pause button isnt in the form itself
               form.parentElement.querySelector("input[name=pauseDraftBtn]").checked = data.draftPaused;
            }
        }
    })
    $.ajax({url: apiBaseUrl + "leagues/" + leagueId + "/users",
        dataType: "json",
        type: "GET",
        success: function(data){
            var userNamesToIds = new Map();
            data.forEach((u) => userNamesToIds.set(u.username, u.userId));
            leaguesToUsers.set(leagueId, userNamesToIds);
            console.log("leaguesToUsers:")
            console.log(leaguesToUsers)
        }
    })
});

$('.updateForm').on('submit', updateForm);

function updateForm(event){
    console.log(event)
    event.preventDefault();
    var form = event.currentTarget;
    var leagueId = form.querySelector("input[name='league_id']").value
    var url = apiBaseUrl + "leagues/" + leagueId + "?apiKey=" + apiKey;
    var draft = {'draftStart': form.querySelector("input[name='start']").value,
                 'nextDraftDeadline': form.querySelector("input[name='nextDeadline']").value,
                 'choiceTimer': parseInt(form.querySelector("input[name='timer']").value),
                 'manualDraft': form.querySelector("input[name=manualDraftBtn]").checked
                 };
    var draftOrderUpdates = form.querySelector("input[name=order]").value;
    if (draftOrderUpdates){
        var split = draftOrderUpdates.split(",");
        draft.order = split.map((name) => parseInt(leaguesToUsers.get(leagueId).get(name)));
    }
    var data = {'league': {'leagueName': form.querySelector("input[name='name']").value},
                'draft': draft
        };
    console.log(data)
    console.log(JSON.stringify(data))
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
                 'choiceTimer': parseInt(form.querySelector("input[name='timer']").value),
                 'manualDraft': form.querySelector("input[name=manualDraftBtn]").checked
        };
    $.ajax({
        url: url,
        dataType: "json",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(data),
        success: function(data){
            Swal.fire({
             title: "Success!",
              type: "success"
            }).then(function(){window.location.reload(false);})
            // Easier to just reload page, than redraw forms
        },
        error: function(jqxhr, textStatus, errorThrown){
            Swal.fire(jqxhr.responseText, '', 'error');
        }
    });
}

function togglePaused(event){
     var leagueId = event.dataset.id;
     var url = apiBaseUrl + "leagues/" + leagueId + "?apiKey=" + apiKey;
     var data = {'draft': {'paused': event.checked}};
     $.ajax({
        url: url,
        dataType: "json",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(data),
        success: function(data){
            Swal.fire({
             title: "Success!",
              type: "success"
            }).then(function(){window.location.reload(false);})
            // Easier to just reload page, than redraw forms
        },
        error: function(jqxhr, textStatus, errorThrown){
            Swal.fire(jqxhr.responseText, '', 'error');
        }
    });
}

$(".generateDraftOrderBtn").click(generateDraftOrderOnclick);

function generateDraftOrderOnclick(event){
    console.log(event)
    var leagueId = event.currentTarget.dataset.id;
    $.ajax({
        url: apiBaseUrl + "leagues/" + leagueId + "/generateDraftOrder?apiKey=" + apiKey,
        dataType: "json",
        type: "POST",
        contentType: "application/json",
        success: function(data){
            Swal.fire({
             title: "Success!",
              type: "success"
            })
        },
        error: function(jqxhr, textStatus, errorThrown){
            Swal.fire(jqxhr.responseText, '', 'error');
        }
    });
}