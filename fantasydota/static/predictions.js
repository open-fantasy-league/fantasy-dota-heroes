var predictionsUrl;
getLeagueInfo(false, false, false, false).then(makePredictions);
var matchIdToScores = new Map();

function makePredictions(){
    $("#leagueLink").attr('href', league.url);
    $("#leagueLink").text(league.name);
    var r = new Array(), j = -1;
    console.log(league)
    if (league.currentPeriod){
        for(var i=1; i<=league.numPeriods; i++){
            r[++j] = '<li><a href="/predictions?period=';
            r[++j] = i;
            r[++j] = '">Week ';
            r[++j] = i;
            r[++j] = '</a></li>';
        }
    }
    $("#periodDropdown").append(r.join(''));
    $("#predictionWinMoney").text(league.predictionWinMoney);
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
    predictionsUrl = apiBaseUrl + "results/leagues/" + leagueId + "/predictions/" + userId + "?";
    if (period != 0){
        predictionsUrl = predictionsUrl + "&period=" + period;
    }

    $.ajax({url: resultsUrl,
                type: "GET",
                dataType: "json",
                success: function(data){
                    var r = new Array(), j = -1;
                    $.each(data, function(key, series){
                        var match = series.matches[0].match;
                        var thisSeries = series.series;
                        var teamOneBasic = thisSeries.teamOne.replace(/[ &]/g, '').toLowerCase();
                        var teamTwoBasic = thisSeries.teamTwo.replace(/[ &]/g, '').toLowerCase();
                        if (match.matchTeamOneFinalScore != null && match.matchTeamOneFinalScore != undefined){
                            matchIdToScores.set(match.matchId, [match.matchTeamOneFinalScore, match.matchTeamTwoFinalScore])
                        }
                        r[++j] = '<div class="row" style="height: 100%">'
                        r[++j] = '<div class="card-panel horizontal matchRow center-align ';
                        r[++j] = teamOneBasic + teamTwoBasic;
                        r[++j] = '" id="match';
                         r[++j] = match.matchId;
                        r[++j] = '"><span class="teamOne col s4 ';
                        r[++j] = teamOneBasic;
                        r[++j] = '"><strong>';
                        r[++j] = thisSeries.teamOne;
                        r[++j] = '</strong></span>';
                        r[++j] = '<div style="width: 180px;background-color: black;" class="card-panel horizontal predictionRow col s4 ';
                        r[++j] = match.started ? ' disabled" ' : ' active" ';
                        r[++j] = 'data-matchId=';
                        r[++j] = match.matchId;
                        r[++j] = '><strong><input class="col s5 center scoreboardfont" style="-moz-appearance: textfield" ';
                        r[++j] = match.started ? ' disabled=true' : "";
                        r[++j] = '  type="text" id="teamOneScorePredict-';
                        r[++j] = match.matchId;
                        r[++j] = '">';
                        r[++j] = '<input style="color:#ff9900" class="col s2 center scoreboardfont" type="text" value=":" disabled><input class="col s5 center scoreboardfont" style="-moz-appearance: textfield" ';
                        r[++j] = match.started ? ' disabled=true' : "";
                        r[++j] = ' type="text" id="teamTwoScorePredict-';
                        r[++j] = match.matchId;
                        r[++j] = '"></strong>';
                        r[++j] = '</div>';
                        r[++j] = '<span class="teamTwo hide-on-small-only col s4 right ';
                        r[++j] = teamTwoBasic;
                        r[++j] = '"><strong>';
                        r[++j] = thisSeries.teamTwo;
                        r[++j] = '</strong></span></div></div>';
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
                    $.each(data, function(key, entry){
                        var teamOneScorePredict = $("#teamOneScorePredict-" + entry.matchId);
                        var teamTwoScorePredict = $("#teamTwoScorePredict-" + entry.matchId);
                        var scores = matchIdToScores.get(entry.matchId);
                        if (teamOneScorePredict){
                            var out = entry.teamOneScore;
                            if (scores){
                                out = out + " <" + scores[0] + ">";
                            }
                            teamOneScorePredict.val(out);

                        };
                        if (teamTwoScorePredict){
                            var out = entry.teamTwoScore;
                            if (scores){
                                out = out + " <" + scores[1] + ">";
                            }
                            teamTwoScorePredict.val(out);
                            };
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
    $.ajax({url: "/prediction_proxy",
                    type: "POST",
                    dataType: "json",
                    data: JSON.stringify(data),
                    contentType: "application/json",
                    success: function(){swal({
             title: "Success",
              type: "success",
              timer: 500
            })},
                    error: function(jqxhr, textStatus, errorThrown){
            Swal.fire({'text': jqxhr.responseText, 'type': 'error'});
        }
            });
}

$("#predictBtn").click(updatePredictions);