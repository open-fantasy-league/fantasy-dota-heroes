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
                    $.each(data, function(key, match){
                        r[++j] = '<div class="card-panel horizontal matchRow vert-align" id="match';
                         r[++j] = match.matchId;
                        r[++j] = '"><span class="teamOne col s3"><strong>';
                        r[++j] = match.teamOne;
                        r[++j] = '</strong></span>';
                        r[++j] = '<span class="predictionRow center-align col s3 ';
                        r[++j] = match.predictionsDisabled ? 'disabled" ' : 'active" ';
                        r[++j] = 'data-matchId=';
                        r[++j] = match.matchId;
                        r[++j] = '><input class="col s2" style="-moz-appearance: textfield" ';
                        r[++j] = match.predictionsDisabled ? 'disabled=true' : "";
                        r[++j] = '  type="number" min="0" id="teamOneScorePredict-';
                        r[++j] = match.matchId;
                        r[++j] = '"></input>';
                        if (match.teamOneScore != null && match.teamOneScore != undefined){
                            var score = '(' + match.teamOneScore + ')';
                            r[++j] = score
                        }
                        r[++j] = '<span class="col s1 center-align"> - </span><input class="col s2" style="-moz-appearance: textfield" ';
                        r[++j] = match.predictionsDisabled ? 'disabled=true' : "";
                        r[++j] = ' type="number" min="0" id="teamTwoScorePredict-';
                        r[++j] = match.matchId;
                        r[++j] = '"></input>';
                        if (match.teamTwoScore != null && match.teamTwoScore != undefined){
                            var score = '(' + match.teamTwoScore + ')';
                            r[++j] = score
                        }
                        r[++j] = '</span>';
                        r[++j] = '<span class="teamTwo hide-on-small-only col s3 right"><strong>';
                        r[++j] = match.teamTwo;
                        r[++j] = '</strong></span></div>';
                    })
                    console.log(r[0])
                    console.log(r.join(''));
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
    $.ajax({url: "/prediction_proxy",
                    type: "POST",
                    dataType: "json",
                    data: JSON.stringify(data),
                    contentType: "application/json",
                    success: function(){swal({
             title: "Success",
              icon: "success",
              timer: 500
            })},
                    error: function(jqxhr, textStatus, errorThrown){
            sweetAlert(jqxhr.responseText, '', 'error');
        }
            });
}

$("#predictBtn").click(updatePredictions);