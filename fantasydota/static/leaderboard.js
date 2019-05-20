getLeagueInfo().then(makeLeaderboard);

function makeLeaderboard(){
    var leaderBoardUrl = apiBaseUrl + "leagues/" + leagueId + "/rankings/" + rankBy;
    if (league.currentPeriod){
        leaderBoardUrl = leaderBoardUrl + "?team";
    }
    if (period != 0){
        leaderBoardUrl = leaderBoardUrl + "&period=" + period;
    }
    if (friends.length != 0){
        leaderBoardUrl = leaderBoardUrl + "&users=" + friends.join(",");
    }
    $("#leagueLink").attr('href', league.url);
    $("#leagueLink").text(league.name);
    var r = new Array(), j = -1;
    if (league.currentPeriod){
        for(var i=1; i<=league.currentPeriod.value; i++){
            r[++j] = '<li><a href="/leaderboard?rank_by=';
            r[++j] = rankBy;
            r[++j] = '&mode=';
            r[++j] = mode;
            r[++j] = "&period=";
            r[++j] = i;
            r[++j] = '">Day ';
            r[++j] = i;
            r[++j] = '</a></li>';
        }
    }
    $("#periodDropdown").append(r.join(''));
    $.ajax({url: leaderBoardUrl,
                type: "GET",
                dataType: "json",
                success: function(data){
                    var r = new Array(), j = -1;
                    var tfoot = new Array(), k = -1;
                    console.log(data)
                    r[++j] = '<tr><th class="positionHeader">Position</th><th class="playerHeader">Player</th><th class="rankingHeader">';
                    r[++j] = rankBy;
                    r[++j] = '</th></tr>';
                    $.each(data.rankings, function(key, player) {
                        console.log(key)
                        console.log(player)
                        var isUser = (player.id === userId);
                        appendBothUserRows(isUser, r, tfoot, j++, k++,'<tr class="');
                        appendBothUserRows(isUser, r, tfoot, j++, k++, isUser ? 'userRow' : 'playerRow');
                        if (userId != null){
                            tfoot[k++] = ' outsideRanks';
                        }
                        appendBothUserRows(isUser, r, tfoot, j++, k++,'"><td class="positionHeader">');
                        appendBothUserRows(isUser, r, tfoot, j++, k++,player.rank);
                        if (period == 0){
                            appendBothUserRows(isUser, r, tfoot, j++, k++, progress_arrow(player));
                        }
                        appendBothUserRows(isUser, r, tfoot, j++, k++, '</td><td class="heroHeader"><span style="vertical-align:middle">');
                        if (league.ended && key == 0){
                            r[++j] = '<img src="static/images/dota/trophy.png"/>';
                        }
                        appendBothUserRows(isUser, r, tfoot, j++, k++,player.username);
                        appendBothUserRows(isUser, r, tfoot, j++, k++,'</span><span class="hero_images">');
                        if (player.team){
                        $.each(player.team, function(key2, hero){
                            var imgSrc = "/static/images/dota/" + hero.name.replace(/ /g, "_") + "_icon.png";
                            appendBothUserRows(isUser, r, tfoot, j++, k++,'<img src="');
                            appendBothUserRows(isUser, r, tfoot, j++, k++,imgSrc);
                            appendBothUserRows(isUser, r, tfoot, j++, k++,'" title="');
                            appendBothUserRows(isUser, r, tfoot, j++, k++,hero.name)
                            appendBothUserRows(isUser, r, tfoot, j++, k++,'"/>');
                        })
                        }
                        appendBothUserRows(isUser, r, tfoot, j++, k++,'</span></td><td class="rankingHeader">');
                        appendBothUserRows(isUser, r, tfoot, j++, k++,player.value);
                        appendBothUserRows(isUser, r, tfoot, j++, k++,'</td></tr>');
                    })
                    $("#leaderboardTable").find("tbody").html(r.concat(tfoot).join(''));
                },
                error: function(data){
                    sweetAlert("Something went wrong. oops!", '', 'error');
                }
            }).then(fillMatches);
        }

function appendBothUserRows(isUser, r, tfoot, j, k, html){
    r[j] = html;
    if (isUser){
        tfoot[k] = html;
    }
}

function fillMatches(){
    if (period == 0){
        return
    }
    var resultsUrl = apiBaseUrl + "results/leagues/" + leagueId + "?";
    if (period != 0){
        resultsUrl = resultsUrl + "&period=" + period;
    }
    function sorted(a, b){
    }

    $.ajax({url: resultsUrl,
                type: "GET",
                dataType: "json",
                success: function(data){
                    var r = new Array(), j = -1;
                    $.each(data, function(key, entry){
                        var match = entry.match;
                        var radiantPicks = entry.results.filter(function(x){return x.isTeamOne && x.stats.picks}).sort(function(a, b){return a.stats.points - b.stats.points});
                        var radiantBans = entry.results.filter(function(x){return x.isTeamOne && x.stats.bans}).sort(function(a, b){return a.stats.points - b.stats.points});
                        var direPicks = entry.results.filter(function(x){return !x.isTeamOne && x.stats.picks}).sort(function(a, b){return b.stats.points - a.stats.points});
                        var direBans = entry.results.filter(function(x){return !x.isTeamOne && x.stats.bans}).sort(function(a, b){return b.stats.points - a.stats.points});
                        console.log(match.id)
                        r[j++] = '<div class="section pointerCursor matchRow" id="match' + match.id + '">';
                        r[j++] = '<div class="row"><span class="radiantTeam">';
                        if (match.teamOneVictory){
                            r[j++] = '<strong>';
                            r[j++] = match.teamOne;
                            r[j++] = '</strong>';
                        }
                        else{
                            r[j++] = match.teamOne;
                        }
                        r[j++] = '</span><span class="direTeam right hide-on-small-only">';
                        if (!match.teamOneVictory){
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
                            r[j++] = pick.stats.points;
                            r[j++] = '</span>';
                        })
                        r[j++] = '</div><div class="right hide-on-small-only">';
                        $.each(direPicks, function(key2, pick){
                            r[j++] = '<span class="';
                            r[j++] = pick.stats.points >= 0 ? 'positive' : 'negative';
                            r[j++] = '"style="display: inline-block; width: 32px; text-align: center;">';
                            r[j++] = pick.stats.points >= 0 ? '+' : '-';
                            r[j++] = pick.stats.points;
                            r[j++] = '</span>';
                        })
                        r[j++] = '</div></div><div class="row"><div class="left">';
                        $.each(radiantPicks, function(key2, pick){
                            var imgSrc = "/static/images/dota/" + pick.pickee.replace(/ /g, "_") + "_icon.png";
                            r[j++] = '<img src="';
                            r[j++] = imgSrc;
                            r[j++] = '" title="';
                            r[j++] = pick.pickee;
                            r[j++] = '" />';
                        })
                        r[j++] = '</div><div class="right hide-on-small-only">';
                        $.each(direPicks, function(key2, pick){
                            var imgSrc = "/static/images/dota/" + pick.pickee.replace(/ /g, "_") + "_icon.png";
                            r[j++] = '<img src="';
                            r[j++] = imgSrc;
                            r[j++] = '" title="';
                            r[j++] = pick.pickee;
                            r[j++] = '" />';
                        })
                        r[j++] = '</div></div><div class="row" style="margin-bottom: 0px"><div class="left">';
                        $.each(radiantBans, function(key2, pick){
                            var imgSrc = "/static/images/dota/" + pick.pickee.replace(/ /g, "_") + "_icon.png";
                            r[j++] = '<img class="banIcon" src="';
                            r[j++] = imgSrc;
                            r[j++] = '" title="';
                            r[j++] = pick.pickee;
                            r[j++] = '" />';
                        })
                        r[j++] = '</div><div class="right hide-on-small-only">';
                        $.each(direBans, function(key2, pick){
                            var imgSrc = "/static/images/dota/" + pick.pickee.replace(/ /g, "_") + "_icon.png";
                            r[j++] = '<img class="banIcon" src="';
                            r[j++] = imgSrc;
                            r[j++] = '" title="';
                            r[j++] = pick.pickee;
                            r[j++] = '" />';
                        })
                        r[j++] = '</div></div><div class="row"><div class="left">';
                        $.each(radiantBans, function(key2, pick){
                            r[j++] = '<span class="';
                            r[j++] = pick.stats.points >= 0 ? 'positive' : 'negative';
                            r[j++] = '"style="display: inline-block; width: 32px; text-align: center;">';
                            r[j++] = pick.stats.points >= 0 ? '+' : '-';
                            r[j++] = pick.stats.points;
                            r[j++] = '</span>';
                        })
                        r[j++] = '</div><div class="right hide-on-small-only">';
                        $.each(direBans, function(key2, pick){
                            r[j++] = '<span class="';
                            r[j++] = pick.stats.points >= 0 ? 'positive' : 'negative';
                            r[j++] = '"style="display: inline-block; width: 32px; text-align: center;">';
                            r[j++] = pick.stats.points >= 0 ? '+' : '-';
                            r[j++] = pick.stats.points;
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
                            r[j++] = pick.stats.points;
                            r[j++] = '</span>';
                        })
                        r[j++] = '</div></div><div class="row"><div class="left">';
                        $.each(direPicks, function(key2, pick){
                            var imgSrc = "/static/images/dota/" + pick.pickee.replace(/ /g, "_") + "_icon.png";
                            r[j++] = '<img src="';
                            r[j++] = imgSrc;
                            r[j++] = '" title="';
                            r[j++] = pick.pickee;
                            r[j++] = '" />';
                        })
                        r[j++] = '</div></div><div class="row" style="margin-bottom: 0px"><div class="left">';
                        $.each(direBans, function(key2, pick){
                            var imgSrc = "/static/images/dota/" + pick.pickee.replace(/ /g, "_") + "_icon.png";
                            r[j++] = '<img class="banIcon" src="';
                            r[j++] = imgSrc;
                            r[j++] = '" title="';
                            r[j++] = pick.pickee;
                            r[j++] = '" />';
                        })
                        r[j++] = '</div></div><div class="row"><div class="left">';
                        $.each(direBans, function(key2, pick){
                            r[j++] = '<span class="';
                            r[j++] = pick.stats.points >= 0 ? 'positive' : 'negative';
                            r[j++] = '"style="display: inline-block; width: 32px; text-align: center;">';
                            r[j++] = pick.stats.points >= 0 ? '+' : '-';
                            r[j++] = pick.stats.points;
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
    if (player.previousRank && friends.length == 0){
        var diff = player.previousRank - player.rank;
        if (diff == 0){
                return " <span>&#8660;</span>";
        }
        else if (diff > 5){
                return ' <span class="upMyArrow">&#8657;</span>';
                }
        else if (diff < -5){
                return ' <span class="downMyArrow">&#8659;</span>';
                }
        else if (diff > 0){
                return ' <span class="supMyArrow">&#8663;</span>';
                }
        else {
                return ' <span class="sdownMyArrow">&#8664;</span>';
        }
    }
    else return '';
}
