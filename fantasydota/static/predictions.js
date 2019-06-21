var predictionsUrl;
getLeagueInfo().then(makePredictions);

function makePredictions(){
    $("#leagueLink").attr('href', league.url);
    $("#leagueLink").text(league.name);
    var r = new Array(), j = -1;
    console.log(league)
    if (league.currentPeriod){
        console.log(league.periods.length)
        for(var i=1; i<=league.periods.length; i++){
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
                        r[++j] = '<div class="row" style="height: 100%">'
                        r[++j] = '<div class="card-panel horizontal matchRow vert-align center-align valign-wrapper" id="match';
                         r[++j] = match.matchId;
                        r[++j] = '"><span class="teamOne col s3 valign"><strong>';
                        r[++j] = thisSeries.teamOne;
                        r[++j] = '</strong></span>';
                        r[++j] = '<div style="width: 180px;" class="card-panel horizontal predictionRow center-align col s3 scoreboardfont valign';
                        r[++j] = match.started ? ' disabled" ' : ' active" ';
                        r[++j] = 'data-matchId=';
                        r[++j] = match.matchId;
                        r[++j] = '><input class="col s3 center" style="-moz-appearance: textfield" ';
                        r[++j] = match.started ? ' disabled=true' : "";
                        r[++j] = '  type="number" min="0" id="teamOneScorePredict-';
                        r[++j] = match.matchId;
                        r[++j] = '">';
                        if (match.teamOneMatchScore != null && match.teamOneMatchScore != undefined){
                            var score = '(' + match.teamOneMatchScore + ')';
                            r[++j] = score
                        }
                        r[++j] = '<input style="color:#ff9900" class="col s3 center" type="text" value=":" disabled><input class="col s3 center" style="-moz-appearance: textfield" ';
                        r[++j] = match.started ? ' disabled=true' : "";
                        r[++j] = ' type="number" min="0" id="teamTwoScorePredict-';
                        r[++j] = match.matchId;
                        r[++j] = '">';
                        if (match.teamTwoMatchScore != null && match.teamTwoMatchScore != undefined){
                            var score = '(' + match.teamTwoMatchScore + ')';
                            r[++j] = score
                        }
                        r[++j] = '</div>';
                        r[++j] = '<span class="teamTwo hide-on-small-only col s3 right valign"><strong>';
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