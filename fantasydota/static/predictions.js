var predictionsUrl;
getLeagueInfo().then(fillMatches);

function makePredictions(){
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
    var resultsUrl = apiBaseUrl + "results/matches/leagues/" + leagueId + "?";
    if (period != 0){
        resultsUrl = resultsUrl + "&period=" + period;
    }
    predictionsUrl = apiBaseUrl + "results/leagues/" + leagueId + "/predictions/" + userId + "?";
    if (period != 0){
        predictionsUrl = predictionsUrl + "&period=" + period;
    }

    $.ajax({url: resultsUrl,
                type: "GET",
                dataType: "json",
                success: function(data){
                    var r = new Array(), j = -1;
                    $.each(data, function(key, entry){
                        var match = entry;
                        r[j++] = '<tr class="row pointerCursor matchRow" id="match' + match.matchId + '">';
                        r[j++] = '<td class="teamOne"><strong>';
                        r[j++] = match.teamOne;
                        r[j++] = '</td></strong>';
                        r[j++] = '<td class="center"><div class="row"><span class="col s2">Result: </span><span class="col s4 center">';
                        r[j++] = match.teamOneScore ? match.teamOneScore : "?";
                        r[j++] = " - ";
                        r[j++] = match.teamTwoScore ? match.teamTwoScore : "?";
                        r[j++] = '</span></div><div class="row predictionRow ';
                        r[j++] = match.predictionsDisabled ? 'disabled" ' : 'active" ';
                        r[j++] = 'data-matchId=';
                        r[j++] = match.matchId;
                        r[j++] = '><span class="col s2">Prediction: </span><input';
                        r[j++] = match.predictionsDisabled ? 'disabled=true' : "";
                        r[j++] = ' class="col s1" type="number" min="0" id="teamOneScorePredict-';
                        r[j++] = match.matchId;
                        r[j++] = '"></input><span class="col s2 center"> - </span><input ';
                        r[j++] = match.predictionsDisabled ? 'disabled=true' : "";
                        r[j++] = ' class="col s1" type="number" min="0" id="teamTwoScorePredict-';
                        r[j++] = match.matchId;
                        r[j++] = '"></input></div></td>';
                        r[j++] = '<td class="awayTeam hide-on-small-only"><strong>';
                        r[j++] = match.teamTwo;
                        r[j++] = '</strong></td></tr>';
                    })
                    $("#predictionsTable").html(r.join(''));
                }
    }).then(fillPredictions)
//    $(".matchRow").each(function() {
//        var elem = $(this)
//        var id_ = elem.attr('id');
//        var match_id = id_.slice(6)
//        elem.click(function() {
//            window.open(statsSitePrefix + match_id)
//        });
//    })
}

function fillPredictions(){
    $.ajax({url: predictionsUrl,
                type: "GET",
                dataType: "json",
                success: function(data){
                    var r = new Array(), j = -1;
                    $.each(data, function(key, entry){
                        var teamOneScorePredict = $("#teamOneScorePredict-" + entry.matchId);
                        var teamTwoScorePredict = $("#teamTwoScorePredict-" + entry.matchId);
                        if (teamOneScorePredict){teamOneScorePredict.val(entry.teamOneScore)};
                        if (teamTwoScorePredict){teamTwoScorePredict.val(entry.teamTwoScore)};
                    })
                }
    })

}

function updatePredictions(){
    var data = {'predictions': []}
    $(".predictionRow.active").each(function(){
    var elem = $(this);
        var inputs = elem.find('input');
        // .value is str so "0" still truthy
        if (inputs[0].value && inputs[1].value){
        data.predictions.push({
                    'matchId': parseInt(elem.attr("data-matchId")), "teamOneScore": inputs[0].valueAsNumber,
                     "teamTwoScore": inputs[1].valueAsNumber
                    });
            }
    })
    $.ajax({url: predictionsUrl,
                    type: "POST",
                    dataType: "json",
                    data: JSON.stringify(data),
                    contentType: "application/json",
                    success: swal({
             title: "Success",
              icon: "success",
              timer: 500
            }),
                    error: function(jqxhr, textStatus, errorThrown){
            sweetAlert(jqxhr.responseText, '', 'error');
        }
            });
}

$("#predictBtn").click(updatePredictions);