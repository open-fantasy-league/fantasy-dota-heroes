signup();
getLeagueInfo(false, false, true, false).then(getCards);

var pickeeUrl = apiBaseUrl + "pickees/" + leagueId;
var pickeeData;
var teamsToPickees = new Map();
var namesToCards = new Map();
function getCards(){
var nextPeriodValue = league.currentPeriod ? league.currentPeriod.value + 1: 1
teamUrl = apiBaseUrl + "leagues/" + leagueId + "/users/" + userId + "?team&stats&period=" + nextPeriodValue;
    $("#leagueLink").attr('href', league.url);
    $("#leagueLink").text(league.name);
    var tabs = $(".tabs");
    var container = $("#clubsContainer");
    $.ajax({url: pickeeUrl, success: function(data){
    pickeeData = data;
                    $.each(data, function(key, pickee){
                        var team = pickee.limitTypes.team;
                        if (teamsToPickees.has(team)){
                            teamsToPickees.get(team).push(pickee);
                        }
                        else{
                            teamsToPickees.set(team, [pickee]);
                        }
                    })
    }}).then(function(){
    $.ajax({url: apiBaseUrl + "teams/league/" + leagueId + "/user/" + userId + "/cards?period=" + nextPeriodValue,
                type: "GET",
                dataType: "json",
                success: function(data){
                    var teamsToCards = new Map();
                    $.each(data, function(key, card){
                        var existing = namesToCards.get(card.name);
                        if (!existing || (existing.color == "BRONZE" && card.color == "SILVER") || card.color == "GOLD"){
                            namesToCards.set(card.name, card);
                        }
                    })

                    var sortedClubs = league.limitTypes.team.map(c => c.name).sort();
                    $.each(sortedClubs, function(key, team){
                        var teamId = team.replace(/[ &]/g, '').toLowerCase();
                        tabs.append('<li class = "tab"><a href = "#' + teamId + '" style="color: #283593">' + team + '</a></li>');
                        containerHtml = [];
                        containerHtml.push('<div id="');
                        containerHtml.push(teamId);
                        containerHtml.push('" class="col s12">');
                        console.log(team)
                        console.log(teamsToPickees)
                        var pickees = teamsToPickees.get(team);
                        pickees.sort(positionNameSort).forEach(p => {
                            cardHtml(containerHtml, namesToCards.get(p.name), p.name, p.limitTypes.team, p.limitTypes.position);
                        })
                        containerHtml.push('</div>');
                        container.append(containerHtml.join(""))
                    })
                    $('.tabs').tabs();
                },
                error: function(jqxhr, textStatus, errorThrown){
                    if (jqxhr.responseText.startsWith("Invalid User ID")){
                        pleaseLogInClick();
                    }
                    else{
                    Swal.fire("Something went wrong. oops!", '', 'error');
                    }
                }
    });
    })
}

function cardHtml(p, player, name, team, position){
    if (!player){
    p.push('<div class="card col s6 m3 playerCardSmol rounded bottomRightParent');
                            p.push('"><div class="card-content"><span class="card-title"><h6><p><span class="playerName centre"><strong>');
                            p.push(name);
                            p.push('</strong></span></p><p><span class="teamName centre">');
                            p.push(team);
                            p.push('</span></p></h6></span><p><span class="left">');
                            p.push(position);
                            p.push('</span></p><div class="card-image"><img src="/static/images/football/placeholder.png"></div><p>');
                            p.push('</div></div>');

    } else{
                            p.push('<div class="card col s6 m3 playerCardSmol rounded bottomRightParent rarity-');
                            p.push(player.colour.toLowerCase());
                            p.push('"><div class="card-content"><span class="card-title"><h6><p><span class="playerName centre"><strong>');
                            p.push(player.name);
                            p.push('</strong></span></p><p><span class="teamName centre">');
                            p.push(player.limitTypes.team);
                            p.push('</span></p></h6></span><p><span class="left">');
                            p.push(player.limitTypes.position);
                            p.push('</span></p><div class="card-image"><img src="/static/images/football/placeholder.png"></div><p>');
                            $.each(player.bonuses, function(bkey, bonus){
                                p.push('<p><i><span class="bonus-rarity-');
                                p.push(player.colour.toLowerCase());
                                p.push('">→');
                                p.push(bonus.name);
                                p.push(' x');
                                p.push(bonus.multiplier);
                                p.push('</span></i></p>');
                            })
                            p.push('</div></div>');
                            }
}    