var teams = new Map();
var pickeeMap = new Map();
var pickees = [];
var ourTeam = [];
var takenPickees = new Set();
var remainingDrafts;
var ourTurn = false;
var now = Date.now();
var nextDraftDeadline;
getLeagueInfo(false, false, false, false).then(setup);


function setup(){
    console.log("in setup")
    if (league.system === 'draft'){
        var draftStart = new Date(league.draftStart);
        if (now < new Date(league.draftStart)){
            $("#draftUnstartedBlock").removeClass('hide');
            $(".draftStartTime").text(draftStart.toISOString());
        }

        getDraftOrder();
        getPickees().then(getDraftQueue);
        getTeams();
        setInterval(updateLoop, 9000);
    }
}

function updateLoop(){
    console.log("looping")
    checkIfUpdated();
}

function checkIfUpdated(){
    now = new Date();
    $(".draftTimer").text(Math.floor((nextDraftDeadline - now) / 1000) + "s ");
    $.ajax({url: apiBaseUrl + "transfers/leagues/" + leagueId + "/draftOrderCount",
            type: "GET",
            dataType: "json",
            success: function(data){
                console.log(data)
                console.log(remainingDrafts)
                if (data < remainingDrafts){
                    remainingDrafts = data;
                            getDraftOrder();
                            getTeams();
                            removeTakenPickees();
                            //getDraftQueue(); theres a race condition where can add queded pickee just after reloading
                            // downside with not updating this is different tabs/browsers get out of sync
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
            nextDraftDeadline = new Date(data.nextDraftDeadline);
            var secondsLeft = Math.floor((nextDraftDeadline - now) / 1000);
            segments.push('<div class="col s2"><div class="row"><h5>Draft Order</h5></div><div style="background-color: black;width:100px" class="card-panel horizontal col s1"><span class="draftTimer scoreboardfont">');
            segments.push(secondsLeft);
            segments.push('s </span></div></div><div class="col s10">');
            $.each(data.order.slice(0, 15), function(i, d){
                var isUs = (userId == d.id);
                segments.push('<div class="draftOrderEntry col s4 m3 l2 chip ');
                if (isUs) segments.push(' green lighten-1');
                 segments.push('">');
                var prefix = i == 0 ? 'now: ' : (i + 1) + ': ';
                if (isUs){
                    segments.push('<strong>');
                    segments.push(prefix);
                    segments.push(d.username);
                    segments.push('</strong>');
                } else{
                    segments.push(prefix);
                    segments.push(d.username);
                }
                segments.push('</div>');
            })
            segments.push('</div>');
            remainingDrafts = data.order.length;
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
            teams.forEach(function(team, key){
                            var segments = [];
                    team.forEach((t) =>{
                        segments.push('<tr><td><strong>');
                        segments.push(t.name);
                        segments.push('</strong></td><td>');
                        segments.push(t.limitTypes.position);
                        segments.push('<img class="teamIcon" src="/static/images/dota/teams/');
                        segments.push(t.limitTypes.team.replace(/[\W_]+/g,"").toLowerCase());
                        segments.push('.png"/>');
                        segments.push('</td></tr>');
                    });
                    $("table[data-userId = " + key + "] > tbody").html(segments.join(''));

            })
        },
        error: function(jqxhr, textStatus, errorThrown){
            Swal.fire("Something went wrong. oops!", '', 'error');
        }
    })
}

function getPickees(){
    return $.ajax({url: apiBaseUrl + "pickees/" + leagueId,
        type: "GET",
        dataType: "json",
        success: function(data){
            pickees = data;
            var segments = [];
            $.each(pickees, function(i, p){
                pickeeMap.set(p.id, p);
                if (!takenPickees.has(p.id)){
                    segments.push('<tr style="cursor: pointer" id="heroesTableHeader"><td class="draftColumn">');
                    segments.push('<button type="submit" name="draftPlayer" class="draftBtn btn waves-effect waves-light" data-id="');
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

function queueHtml(segments, pickeeId){
    var pickee = pickeeMap.get(pickeeId);
    if (pickee && !ourTeam.find((t) => t.id == pickeeId)){
        console.log("queuing " + pickee.name)
        segments.push('<tr><td><button type="submit" class="removeBtn btn waves-effect waves-light" data-id="');
        segments.push(pickeeId);
        segments.push('">Remove</button>');
        segments.push('</td><td><strong>')
        segments.push(pickee.name);
        segments.push('</strong></td><td>');
        segments.push(pickee.limitTypes.position);
        segments.push('<img class="teamIcon" src="/static/images/dota/teams/');
        segments.push(pickee.limitTypes.team.replace(/[\W_]+/g,"").toLowerCase());
        segments.push('.png"/>');
        segments.push('</td></tr>');
    }
    return segments
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
                    queueHtml(segments, d.id);
                })
                var html = segments.join('');
                $("#queueTable > tbody").html(html);
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
                    button.parent().parent().remove();
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
        var pickeeId = parseInt(button.attr('data-id'));
        console.log("pickeeId " + pickeeId)
        $.ajax({url: "/draft_proxy?league_id=" + leagueId,
                type: "POST",
                dataType: "json",
                data: JSON.stringify({'pickeeId': pickeeId, 'method': 'append'}),
                contentType: "application/json",
                success: function(data){
                    var segments = [];
                    queueHtml(segments, pickeeId);
                    var html = segments.join("");
                    console.log(html)
                    $("#queueTable > tbody").append(html);
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

function fillTeamCollapsibles(){
    var holder = $("#teamsCollapsible");

}