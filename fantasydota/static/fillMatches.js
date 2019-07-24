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
                    $.each(data, function(key, d){
                    var series = d.series;
                    console.log(d)
                    $.each(d.matches, function(key, entry){
                        var match = entry.match;
                        var radiantPicks = entry.results.filter(function(x){return x.isTeamOne && x.stats.picks}).sort(function(a, b){return a.stats.points - b.stats.points});
                        var radiantBans = entry.results.filter(function(x){return x.isTeamOne && x.stats.bans}).sort(function(a, b){return a.stats.points - b.stats.points});
                        var direPicks = entry.results.filter(function(x){return !x.isTeamOne && x.stats.picks}).sort(function(a, b){return b.stats.points - a.stats.points});
                        var direBans = entry.results.filter(function(x){return !x.isTeamOne && x.stats.bans}).sort(function(a, b){return b.stats.points - a.stats.points});
                        console.log(match.matchId)
                        r[++j] = '<div class="section pointerCursor matchRow" id="match' + match.matchId + '">';
                        r[++j] = '<div class="row"><span class="radiantTeam">';
                        if (match.teamOneFinalScore){
                            r[++j] = '<strong>';
                            r[++j] = series.teamOne;
                            r[++j] = '</strong>';
                        }
                        else{
                            r[++j] = series.teamOne;
                        }
                        r[++j] = '</span><span class="direTeam right hide-on-small-only">';
                        if (!match.teamOneFinalScore){
                            r[++j] = '<strong>';
                            r[++j] = series.teamTwo;
                            r[++j] = '</strong>';
                        }
                        else{
                            r[++j] = series.teamTwo;
                        }
                        r[++j] = '</span></div><div class="row" style="margin-bottom: 0px"><div class="left">';
                        $.each(radiantPicks, function(key2, pick){
                            r[++j] = '<span class="';
                            r[++j] = pick.stats.points >= 0 ? 'positive' : 'negative';
                            r[++j] = '"style="display: inline-block; width: 32px; text-align: center;">';
                            r[++j] = pick.stats.points >= 0 ? '+' : '-';
                            r[++j] = pick.stats.points;
                            r[++j] = '</span>';
                        })
                        r[++j] = '</div><div class="right hide-on-small-only">';
                        $.each(direPicks, function(key2, pick){
                            r[++j] = '<span class="';
                            r[++j] = pick.stats.points >= 0 ? 'positive' : 'negative';
                            r[++j] = '"style="display: inline-block; width: 32px; text-align: center;">';
                            r[++j] = pick.stats.points >= 0 ? '+' : '-';
                            r[++j] = pick.stats.points;
                            r[++j] = '</span>';
                        })
                        r[++j] = '</div></div><div class="row"><div class="left">';
                        $.each(radiantPicks, function(key2, pick){
                            var imgSrc = "/static/images/dota/" + pick.name.replace(/ /g, "_") + "_icon.png";
                            r[++j] = '<img src="';
                            r[++j] = imgSrc;
                            r[++j] = '" title="';
                            r[++j] = pick.name;
                            r[++j] = '" />';
                        })
                        r[++j] = '</div><div class="right hide-on-small-only">';
                        $.each(direPicks, function(key2, pick){
                            var imgSrc = "/static/images/dota/" + pick.name.replace(/ /g, "_") + "_icon.png";
                            r[++j] = '<img src="';
                            r[++j] = imgSrc;
                            r[++j] = '" title="';
                            r[++j] = pick.name;
                            r[++j] = '" />';
                        })
                        r[++j] = '</div></div><div class="row" style="margin-bottom: 0px"><div class="left">';
                        $.each(radiantBans, function(key2, pick){
                            var imgSrc = "/static/images/dota/" + pick.name.replace(/ /g, "_") + "_icon.png";
                            r[++j] = '<img class="banIcon" src="';
                            r[++j] = imgSrc;
                            r[++j] = '" title="';
                            r[++j] = pick.name;
                            r[++j] = '" />';
                        })
                        r[++j] = '</div><div class="right hide-on-small-only">';
                        $.each(direBans, function(key2, pick){
                            var imgSrc = "/static/images/dota/" + pick.name.replace(/ /g, "_") + "_icon.png";
                            r[++j] = '<img class="banIcon" src="';
                            r[++j] = imgSrc;
                            r[++j] = '" title="';
                            r[++j] = pick.name;
                            r[++j] = '" />';
                        })
                        r[++j] = '</div></div><div class="row"><div class="left">';
                        $.each(radiantBans, function(key2, pick){
                            r[++j] = '<span class="';
                            r[++j] = pick.stats.points >= 0 ? 'positive' : 'negative';
                            r[++j] = '"style="display: inline-block; width: 32px; text-align: center;">';
                            r[++j] = pick.stats.points >= 0 ? '+' : '-';
                            r[++j] = pick.stats.points;
                            r[++j] = '</span>';
                        })
                        r[++j] = '</div><div class="right hide-on-small-only">';
                        $.each(direBans, function(key2, pick){
                            r[++j] = '<span class="';
                            r[++j] = pick.stats.points >= 0 ? 'positive' : 'negative';
                            r[++j] = '"style="display: inline-block; width: 32px; text-align: center;">';
                            r[++j] = pick.stats.points >= 0 ? '+' : '-';
                            r[++j] = pick.stats.points;
                            r[++j] = '</span>';
                        })
                        r[++j] = '</div></div><div class="columniseMobileView hide-on-med-and-up"><div class="row"><span class="direTeam left">';
                        if (!match.teamOneFinalScore){
                            r[++j] = '<strong>';
                            r[++j] = match.teamTwo;
                            r[++j] = '</strong>';
                        }
                        else{
                            r[++j] = match.teamTwo;
                        }
                        r[++j] = '</span></div><div class="row" style="margin-bottom: 0px"><div class="left">';
                        $.each(direPicks, function(key2, pick){
                            r[++j] = '<span class="';
                            r[++j] = pick.stats.points >= 0 ? 'positive' : 'negative';
                            r[++j] = '"style="display: inline-block; width: 32px; text-align: center;">';
                            r[++j] = pick.stats.points >= 0 ? '+' : '-';
                            r[++j] = pick.stats.points;
                            r[++j] = '</span>';
                        })
                        r[++j] = '</div></div><div class="row"><div class="left">';
                        $.each(direPicks, function(key2, pick){
                            var imgSrc = "/static/images/dota/" + pick.name.replace(/ /g, "_") + "_icon.png";
                            r[++j] = '<img src="';
                            r[++j] = imgSrc;
                            r[++j] = '" title="';
                            r[++j] = pick.name;
                            r[++j] = '" />';
                        })
                        r[++j] = '</div></div><div class="row" style="margin-bottom: 0px"><div class="left">';
                        $.each(direBans, function(key2, pick){
                            var imgSrc = "/static/images/dota/" + pick.name.replace(/ /g, "_") + "_icon.png";
                            r[++j] = '<img class="banIcon" src="';
                            r[++j] = imgSrc;
                            r[++j] = '" title="';
                            r[++j] = pick.name;
                            r[++j] = '" />';
                        })
                        r[++j] = '</div></div><div class="row"><div class="left">';
                        $.each(direBans, function(key2, pick){
                            r[++j] = '<span class="';
                            r[++j] = pick.stats.points >= 0 ? 'positive' : 'negative';
                            r[++j] = '"style="display: inline-block; width: 32px; text-align: center;">';
                            r[++j] = pick.stats.points >= 0 ? '+' : '-';
                            r[++j] = pick.stats.points;
                            r[++j] = '</span>';
                        })
                        r[++j] = '</div></div></div></div><div class="divider"></div>';
                    })
                    })
                    $("#matchesContainer").html(r.join(''));
                }
    })
    $(".matchRow").each(function() {
        var elem = $(this)
        var id_ = elem.attr('id');
        var match_id = id_.slice(6)
        elem.click(function() {
            window.open("https://www.opendota.com/matches/" + match_id)
        });
    })
}
fillMatches();