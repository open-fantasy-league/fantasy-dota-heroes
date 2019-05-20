getLeagueInfo().then(makeLeaderboard);

function makePredictions){
    $("#leagueLink").attr('href', league.url);
    $("#leagueLink").text(league.name);
    var r = new Array(), j = -1;
    if (league.currentPeriod){
        for(var i=1; i<=league.currentPeriod.value + 1; i++){
            r[++j] = '<li><a href="/predictions?period=';
            r[++j] = i;
            r[++j] = '">Week ';
            r[++j] = i;
            r[++j] = '</a></li>';
        }
    }
    $("#periodDropdown").append(r.join(''));
    fillMatches();
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
                        console.log(match.id)
                        r[j++] = '<div class="section pointerCursor matchRow" id="match' + match.id + '">';
                        r[j++] = '<div class="row"><span class="left teamOne">';
                        r[j++] = match.teamOne;
                        r[j++] = '</span>';
                        r[j++] = '<div class="col s4"><span class="centre">Result: ';
                        r[j++] = match.teamOneScore ? match.teamOneScore : "?";
                        r[j++] = " - ";
                        r[j++] = match.teamTwoScore ? match.teamTwoScore : "?";
                        r[j++] = '</span><span class="centre">Prediction: <span id="teamOneScorePredict-';
                        r[j++] = match.id;
                        r[j++] = '"></span> - <span id="teamTwoScorePredict-';
                        r[j++] = match.id;
                        r[j++] = '"></span></span></div>';
                        r[j++] = '<span class="awayTeam right hide-on-small-only">';
                        r[j++] = match.teamTwo;
                        r[j++] = '</span></div></div><div class="divider"></div>';
                    })
                    $("#matchesContainer").html(r.join(''));
                }
    }).then(fillPredictions)
    $(".matchRow").each(function() {
        var elem = $(this)
        var id_ = elem.attr('id');
        var match_id = id_.slice(6)
        elem.click(function() {
            window.open(statsSitePrefix + match_id)
        });
    })
}

function fillPredictions(){
    var predictionsUrl = apiBaseUrl + "results/leagues/" + leagueId + "/predictions/" + userId + "?";
    if (period != 0){
        predictionsUrl = predictionsUrl + "&period=" + period;
    }
    $.ajax({url: predictionsUrl,
                type: "GET",
                dataType: "json",
                success: function(data){
                    var r = new Array(), j = -1;
                    $.each(data, function(key, entry){
                        var teamOneScorePredict = $("#teamOneScorePredict-" + entry.matchId);
                        var teamTwoScorePredict = $("#teamTwoScorePredict-" + entry.matchId);
                        if (teamOneScorePredict){teamOneScorePredict.text(entry.teamOneScore)};
                        if (teamTwoScorePredict){teamTwoScorePredict.text(entry.teamTwoScore)};
                    })
                }
    })

}