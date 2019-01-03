$.ajax({url: apiBaseUrl + "leagues/" + leagueId,
    dataType: "json",
    type: "GET",
    success: function(data){
        league = data;
        console.log(league)
    }
}).then(makeLeaderboard)

function makeLeaderboard(){
    var leaderBoardUrl = apiBaseUrl + "leagues/" + leagueId + "/rankings/" + rankBy + "?team";
    if (period != "tournament" && period != "0"){
        leaderBoardUrl = leaderBoardUrl + "&period=" + period;
    }
    $("#leagueLink").attr('href', league.url);
    $("#leagueLink").text(league.name);
    var periodDropdown = $("#periodDropdown");
    var periodHtml = "";
    var r = new Array(), j = -1;
    for(var i=1; i<=league.currentPeriod.value; i++){
        r[++j] = '<li><a href="/leaderboard?rank_by=';
        r[++j] = rankBy;
        r[++j] = '&mode=';
        r[++j] = mode;
        r[++j] = "&period=";
        r[++j] = i;
        r[++j] = '>Day';
        r[++j] = i;
        r[++j] = '</a></li>';
    }
    periodDropdown.append(r.join(''));
    console.log($("#leaderboardTable").find("tbody"))
    $.ajax({url: leaderBoardUrl,
                type: "GET",
                dataType: "json",
                success: function(data){
                    var r = new Array(), j = -1;
                    console.log(data)
                    r[++j] = '<tr><th class="positionHeader">Position</th><th class="playerHeader">Player</th><th class="rankingHeader">';
                    r[++j] = rankBy;
                    r[++j] = '</th></tr>';
                    $.each(data.rankings, function(key, player) {
                        console.log(key)
                        console.log(player)
                        console.log(userId)
                        var isUser = (player.externalId === userId);
                        r[++j] = '<tr class="';
                        r[++j] = isUser ? 'userRow' : 'playerRow';
                        r[++j] = '"><td class="positionEntry">';
                        r[++j] = player.rank;
                        if (period == "tournament"){
                            r[++j] = progress_arrow(player);
                        }
                        r[++j] = '</td><td class="heroEntry"><span style="vertical-align:middle">';
                        if (league.ended && key == 0){
                            r[++j] = '<img src="static/images/dota/trophy.png"/>';
                        }
                        r[++j] = player.username;
                        r[++j] = '</span><span class="hero_images">';
                        $.each(player.team, function(key2, hero){
                            var imgSrc = "/static/images/dota/" + hero.name.replace(" ", "_") + "_icon.png";
                            r[++j] = '<img src="';
                            r[++j] = imgSrc;
                            r[++j] = '" title="';
                            r[++j] = hero.name;
                            r[++j] = '"/>';
                        })
                        r[++j] = '</span></td><td class="rankingEntry">';
                        r[++j] = player.value;
                        r[++j] = '</td></tr>';
                    })
                    $("#leaderboardTable").find("tbody").html(r.join(''));
                },
                failure: function(data){
                    sweetAlert("Something went wrong. oops!", '', 'error');
                }
            }).then(fillMatches);
        }

function fillMatches(){
    var resultsUrl = apiBaseUrl + "results/" + leagueId + "?";
    if (period != "tournament" && period != "0"){
        resultsUrl = resultsUrl + "&period=" + period;
    }

    $.ajax({url: resultsUrl,
                type: "GET",
                dataType: "json",
                success: function(data){
                    var r = new Array(), j = -1;
                    $.each(data, function(key, entry){
                        var match = entry.match;
                        var radiantPicks = entry.results.filter(function(x){return x.isTeamOne && x.stats.picks});
                        var radiantBans = entry.results.filter(function(x){return x.isTeamOne && x.stats.bans});
                        var direPicks = entry.results.filter(function(x){return !x.isTeamOne && x.stats.picks});
                        var direBans = entry.results.filter(function(x){return !x.isTeamOne && x.stats.bans});
                        console.log(match.id)
                        r[j++] = '<div class="section pointerCursor matchRow" id="match' + match.id + '">';
                        r[j++] = '<div class="row"><span class="radiantTeam">';
                        if (match.isTeamOneVictory){
                            r[j++] = '<strong>';
                            r[j++] = match.teamOne;
                            r[j++] = '</strong>';
                        }
                        else{
                            r[j++] = match.teamOne;
                        }
                        r[j++] = '</span><span class="direTeam right hide-on-small-only">';
                        if (!match.isTeamOneVictory){
                            r[j++] = '<strong>';
                            r[j++] = match.teamTwo;
                            r[j++] = '</strong>';
                        }
                        else{
                            r[j++] = match.teamTwo;
                        }
                        r[j++] = '</span></div><div class="row" style="margin-bottom: 0px"><div class="left">';
                        $.each(radiantPicks, function(key2, pick){
                            r[j++] = '<span class="';
                            r[j++] = pick.stats.points >= 0 ? 'positive' : 'negative';
                            r[j++] = '"style="display: inline-block; width: 32px; text-align: center;">';
                            r[j++] = pick.stats.points >= 0 ? '+' : '-';
                            r[j++] = '</span>';
                        })
                        r[j++] = '</div><div class="right hide-on-small-only">';
                        $.each(direPicks, function(key2, pick){
                            r[j++] = '<span class="';
                            r[j++] = pick.stats.points >= 0 ? 'positive' : 'negative';
                            r[j++] = '"style="display: inline-block; width: 32px; text-align: center;">';
                            r[j++] = pick.stats.points >= 0 ? '+' : '-';
                            r[j++] = '</span>';
                        })
                        r[j++] = '</div></div><div class="row"><div class="left">';
                        $.each(radiantPicks, function(key2, pick){
                            var imgSrc = "/static/images/dota/" + pick.pickee.name.replace(" ", "_") + "_icon.png";
                            r[j++] = '<img src="';
                            r[j++] = imgSrc;
                            r[j++] = '" title="';
                            r[j++] = pick.pickee.name;
                            r[j++] = '" />';
                        })
                        r[j++] = '</div><div class="right hide-on-small-only">';
                        $.each(direPicks, function(key2, pick){
                            var imgSrc = "/static/images/dota/" + pick.pickee.name.replace(" ", "_") + "_icon.png";
                            r[j++] = '<img src="';
                            r[j++] = imgSrc;
                            r[j++] = '" title="';
                            r[j++] = pick.pickee.name;
                            r[j++] = '" />';
                        })
                        r[j++] = '</div></div><div class="row" style="margin-bottom: 0px"><div class="left">';
                        $.each(radiantBans, function(key2, pick){
                            var imgSrc = "/static/images/dota/" + pick.pickee.name.replace(" ", "_") + "_icon.png";
                            r[j++] = '<img class="banIcon" src="';
                            r[j++] = imgSrc;
                            r[j++] = '" title="';
                            r[j++] = pick.pickee.name;
                            r[j++] = '" />';
                        })
                        r[j++] = '</div><div class="right hide-on-small-only">';
                        $.each(direBans, function(key2, pick){
                            var imgSrc = "/static/images/dota/" + pick.pickee.name.replace(" ", "_") + "_icon.png";
                            r[j++] = '<img class="banIcon" src="';
                            r[j++] = imgSrc;
                            r[j++] = '" title="';
                            r[j++] = pick.pickee.name;
                            r[j++] = '" />';
                        })
                        r[j++] = '</div></div><div class="row"><div class="left">';
                        $.each(radiantBans, function(key2, pick){
                            r[j++] = '<span class="';
                            r[j++] = pick.stats.points >= 0 ? 'positive' : 'negative';
                            r[j++] = '"style="display: inline-block; width: 32px; text-align: center;">';
                            r[j++] = pick.stats.points >= 0 ? '+' : '-';
                            r[j++] = '</span>';
                        })
                        r[j++] = '</div><div class="right hide-on-small-only">';
                        $.each(direBans, function(key2, pick){
                            r[j++] = '<span class="';
                            r[j++] = pick.stats.points >= 0 ? 'positive' : 'negative';
                            r[j++] = '"style="display: inline-block; width: 32px; text-align: center;">';
                            r[j++] = pick.stats.points >= 0 ? '+' : '-';
                            r[j++] = '</span>';
                        })
                        r[j++] = '</div></div><div class="columniseMobileView hide-on-med-and-up"><div class="row"><span class="direTeam left">';
                        if (!match.isTeamOneVictory){
                            r[j++] = '<strong>';
                            r[j++] = match.teamTwo;
                            r[j++] = '</strong>';
                        }
                        else{
                            r[j++] = match.teamTwo;
                        }
                        r[j++] = '</span></div><div class="row" style="margin-bottom: 0px"><div class="left">';
                        $.each(direPicks, function(key2, pick){
                            r[j++] = '<span class="';
                            r[j++] = pick.stats.points >= 0 ? 'positive' : 'negative';
                            r[j++] = '"style="display: inline-block; width: 32px; text-align: center;">';
                            r[j++] = pick.stats.points >= 0 ? '+' : '-';
                            r[j++] = '</span>';
                        })
                        r[j++] = '</div></div><div class="row"><div class="left">';
                        $.each(direPicks, function(key2, pick){
                            var imgSrc = "/static/images/dota/" + pick.pickee.name.replace(" ", "_") + "_icon.png";
                            r[j++] = '<img src="';
                            r[j++] = imgSrc;
                            r[j++] = '" title="';
                            r[j++] = pick.pickee.name;
                            r[j++] = '" />';
                        })
                        r[j++] = '</div></div><div class="row" style="margin-bottom: 0px"><div class="left">';
                        $.each(direBans, function(key2, pick){
                            var imgSrc = "/static/images/dota/" + pick.pickee.name.replace(" ", "_") + "_icon.png";
                            r[j++] = '<img class="banIcon" src="';
                            r[j++] = imgSrc;
                            r[j++] = '" title="';
                            r[j++] = pick.pickee.name;
                            r[j++] = '" />';
                        })
                        r[j++] = '</div></div><div class="row"><div class="left">';
                        $.each(direBans, function(key2, pick){
                            r[j++] = '<span class="';
                            r[j++] = pick.stats.points >= 0 ? 'positive' : 'negative';
                            r[j++] = '"style="display: inline-block; width: 32px; text-align: center;">';
                            r[j++] = pick.stats.points >= 0 ? '+' : '-';
                            r[j++] = '</span>';
                        })
                        r[j++] = '</div></div></div></div><div class="divider"></div>';
                    })
                    $("#matchesContainer").html(r.join(''));
                }
    })
    $(".matchRow").each(function() {
        var elem = $(this)
        var id_ = elem.attr('id');
        var match_id = id_.slice(6)
        elem.click(function() {
            window.open(statsSitePrefix + match_id)
        });
    })
}


function progress_arrow(player){
    if (player.previousRank){
        var diff = player.previousRank - player.rank;
        if (diff == 0){
                return " <span>&#8660;</span>";
        }
        else if (diff < -5){
                return ' <span class="upMyArrow">&#8657;</span>';
                }
        else if (diff > 5){
                return ' <span class="downMyArrow">&#8659;</span>';
                }
        else if (diff < 0){
                return ' <span class="supMyArrow">&#8663;</span>';
                }
        else {
                return ' <span class="sdownMyArrow">&#8664;</span>';
        }
    }
}