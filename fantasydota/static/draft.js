var teams = new Map();
var pickeeMap = new Map();
var pickees = [];
var ourTeam = [];
var takenPickees = new Set();
var remainingDrafts;
var ourTurn = false;
//signup();
getLeagueInfo(false, false, false, false).then(setup);


function setup(){
    console.log("in setup")
    if (league.system === 'draft'){
        var draftStart = new Date(league.draftStart);
        if (Date.now() < new Date(league.draftStart)){
            $("#draftUnstartedBlock").removeClass('hide');
            $(".draftStartTime").text(draftStart.toISOString());
        }

        getDraftOrder();
        getTeams();
        getDraftQueue();
        getPickees();
        setInterval(updateLoop, 20000);
    }
}

function updateLoop(){
    console.log("looping")
    checkIfUpdated();
}

function checkIfUpdated(){
    $.ajax({url: apiBaseUrl + "transfers/leagues/" + leagueId + "/draftOrderCount",
            type: "GET",
            dataType: "json",
            success: function(data){
                console.log(data)
                if (data < remainingDrafts){
                    remainingDrafts = data;
                            getDraftOrder();
                            getTeams();
                            removeTakenPickees();
                }
            },
            error: function(jqxhr, textStatus, errorThrown){
                Swal.fire("Something went wrong. oops!", '', 'error');
            }
        })
}

function getDraftOrder(){
    $.ajax({url: apiBaseUrl + "transfers/leagues/" + leagueId + "/draftOrder",
        type: "GET",
        dataType: "json",
        success: function(data){
            var segments = [];
            // only show next 12
            $.each(data.order.slice(0, 12), function(i, d){
                segments.push('<div class="draftOrderEntry col s4 m3 l2">');
                if (i == 0){
                    var secondsLeft = Math.floor((new Date(data.nextDraftDeadline) - new Date()) / 1000);
                    segments.push(secondsLeft);
                    segments.push("s ");
                }
                if (userId == d.id){
                    segments.push('<strong>');
                    segments.push(d.username);
                    segments.push('</strong>');
                } else{
                    segments.push(d.username);
                }
                segments.push('</div>');
            })
            remainingDrafts = data.length;
            console.log("ouruser " + userId)
            console.log("data[0].userId " + data.order[0].id)
            ourTurn = data.order[0].id === userId;
            var draftBtns = $(".draftBtn")
            if (ourTurn){
                draftBtns.click(draftOnclick);
                draftBtns.text("Draft");
            }
            else{
                draftBtns.click(appendDraftQueueOnclick);
                draftBtns.text("Queue");
            }
            var draftOrderBlock = $("#draftOrderBlock");
            draftOrderBlock.html(segments.join(''));
            draftOrderBlock.removeClass('hide');
            },
        error: function(jqxhr, textStatus, errorThrown){
            if (jqxhr.responseText.startsWith("Invalid User ID")){
                pleaseLogInClick();
            }
            else{
            Swal.fire("Something went wrong. oops!", '', 'error');
            }
        }
    })
}

function getTeams(){
    $.ajax({url: apiBaseUrl + "teams/league/" + leagueId + "/cards",
        type: "GET",
        dataType: "json",
        success: function(data){
            teams = new Map();
            ourTeam = [];
            $.each(data, function(i, d){
                if (teams.get(d.userId)){
                    teams.get(d.userId).push(d);
                }
                else{
                    teams.set(d.userId, [d]);
                }
                takenPickees.add(d.id);
                if (d.userId === userId){
                    ourTeam.push(d);
                }
            })
            console.log(teams)
            var segments = [];
            $.each(ourTeam, function(i, t){
                segments.push('<div class="row">');
                segments.push(t.name);
                segments.push(' (');
                segments.push(t.limitTypes.position);
                segments.push(')</div>');
            })
            $("#draftTeamCol").html(segments.join(''));
        },
        error: function(jqxhr, textStatus, errorThrown){
            Swal.fire("Something went wrong. oops!", '', 'error');
        }
    })
}

function getPickees(){
    $.ajax({url: apiBaseUrl + "pickees/" + leagueId,
        type: "GET",
        dataType: "json",
        success: function(data){
            pickees = data;
            var segments = [];
            $.each(pickees, function(i, p){
                pickeeMap.set(p.id, p);
                if (!takenPickees.has(p.id)){
                    segments.push('<tr style="cursor: pointer" id="heroesTableHeader"><td class="draftBtn">');
                    segments.push('<button type="submit" name="draftPlayer" class="btn waves-effect waves-light" data-id="');
                    segments.push(p.id);
                    segments.push('">');
                    segments.push(ourTurn ? 'Draft' : 'Queue');
                    segments.push('</button></td><td><strong>');
                    segments.push(p.name);
                    segments.push('</strong></td><td class="positionEntry">');
                    segments.push(p.limitTypes.position);
                    segments.push('</td><td class="teamEntry"><img class="teamIcon" src="/static/images/dota/teams/');
                    segments.push(p.limitTypes.team.replace(/[\W_]+/g,"").toLowerCase());
                    segments.push('.png"/>');
                    segments.push(p.limitTypes.team);
                    segments.push('</td></tr>');
                }
            })
            console.log(segments)
            var html = segments.join('');
            console.log(html)
            $("#pickeeTable").find("tbody").html(html);
            $("[name=draftPlayer]").click(ourTurn ? draftOnclick : appendDraftQueueOnclick);
        },
        error: function(jqxhr, textStatus, errorThrown){
            Swal.fire("Something went wrong. oops!", '', 'error');
        }
    })
}

function getDraftQueue(){
    $.ajax({url: "/draft_proxy?league_id=" + leagueId,
            type: "POST",
            data: JSON.stringify({'method': 'get'}),
            dataType: "json",
            contentType: "application/json",
            success: function(data){
                var segments = [];
                $.each(data.queue, function(i, d){
                    if (!ourTeam.find((t) => t.id == d.id)){
                        segments.push('<div class="row draftQueueEntry"><span>');
                        segments.push(d.name);
                        segments.push('</span><button type="submit" class="removeBtn" data-id="');
                        segments.push(d.id);
                        segments.push('">Remove</button></div>');
                    }
                })
                $("#draftQueue").html(segments.join(''));
                $(".removeBtn").click(removeDraftQueueOnclick);
                console.log("data.autopick" + data.autopick)
                if (data.autopick){
                    $("#autopickBtn").attr('checked', 'true');
                }
                else{
                    $("#autopickBtn").removeAttr('checked');
                }
            },
            error: function(jqxhr, textStatus, errorThrown){
                if (jqxhr.responseText.startsWith("Invalid User ID")){
                    pleaseLogInClick();
                }
                else{
                Swal.fire("Something went wrong. oops!", '', 'error');
                }
            }
        })
}

function removeDraftQueueOnclick(event){
        var button = $(event.currentTarget);
        var removeId = button.attr('data-id');
        $.ajax({url: "/draft_proxy?league_id=" + leagueId,
                type: "POST",
                data: JSON.stringify({'method': 'remove', 'pickeeId': removeId}),
                dataType: "json",
                contentType: "application/json",
                success: function(data){
                    button.parent().remove();
                },
                error: function(jqxhr, textStatus, errorThrown){
                    if (jqxhr.responseText.startsWith("Invalid User ID")){
                        pleaseLogInClick();
                    }
                    else{
                    Swal.fire("Something went wrong. oops!", '', 'error');
                    }
                }
            })
}

function appendDraftQueueOnclick(event){
        var button = $(event.currentTarget);
        var pickeeId = button.attr('data-id');
        console.log("pickeeId " + pickeeId)
        $.ajax({url: "/draft_proxy?league_id=" + leagueId,
                type: "POST",
                dataType: "json",
                data: JSON.stringify({'pickeeId': pickeeId, 'method': 'append'}),
                contentType: "application/json",
                success: function(data){
                    var segments = [];
                    segments.push('<div class="row draftQueueEntry"><span>');
                    segments.push(pickeeMap.get(parseInt(pickeeId)).name);
                    segments.push('</span><button type="submit" class="removeBtn" data-id="');
                    segments.push(pickeeId);
                    segments.push('">Remove</button></div>');
                    $("#draftQueue").append(segments.join(''));
                    $(".removeBtn").click(removeDraftQueueOnclick);
                },
                error: function(jqxhr, textStatus, errorThrown){
                    if (jqxhr.responseText.startsWith("Invalid User ID")){
                        pleaseLogInClick();
                    }
                    else{
                    Swal.fire("Something went wrong. oops!", '', 'error');
                    }
                }
            })
}

function draftOnclick(event){
console.log("draftclick")
    var button = $(event.currentTarget);
    var pickeeId = button.attr('data-id');
    $.ajax({url: "/draft_proxy?league_id=" + leagueId,
        type: "POST",
        data: JSON.stringify({'method': 'draft', 'pickeeId': pickeeId}),
        dataType: "json",
        contentType: "application/json",
        success: function(data){
            window.location.reload();
        },
        error: function(jqxhr, textStatus, errorThrown){
            if (jqxhr.responseText.startsWith("Invalid User ID")){
                pleaseLogInClick();
            }
            else{
            Swal.fire("Something went wrong. oops!", '', 'error');
            }
        }
    })
}

function removeTakenPickees(){
    for (const pid of takenPickees){
    //$.each(takenPickees, function(i, p){
        $("[name='draftPlayer'][data-id='" + pid + "']").parent().remove();
        }
    //})
}

function switchAutopick(event){
    $.ajax({url: "/draft_proxy?league_id=" + leagueId,
        type: "POST",
        data: JSON.stringify({'method': 'autopick', 'set': event.checked ? 'on' : 'off'}),
        dataType: "json",
        contentType: "application/json",
        error: function(jqxhr, textStatus, errorThrown){
            if (jqxhr.responseText.startsWith("Invalid User ID")){
                pleaseLogInClick();
            }
            else{
            Swal.fire("Something went wrong. oops!", '', 'error');
            }
        }
    })
}