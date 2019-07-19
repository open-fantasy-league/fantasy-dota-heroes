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
            r[++j] = '">';
            r[++j] = league.periodDescription;
            r[++j] = ' ';
            r[++j] = i;
            r[++j] = '</a></li>';
        }
    }
    $("#periodDropdown").append(r.join(''));
    $("#predictionPeriodDropdown").text(league.periodDescription);
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
                        var thisSeries = series.series;
                        var teamOneBasic = thisSeries.teamOne.replace(/[\W_]+/g,"").toLowerCase();
                        var teamTwoBasic = thisSeries.teamTwo.replace(/[\W_]+/g,"").toLowerCase();
                        if (thisSeries.seriesTeamOneFinalScore != null && thisSeries.seriesTeamOneFinalScore != undefined){
                            seriesIdToScores.set(thisSeries.seriesId, [thisSeries.seriesTeamOneFinalScore, thisSeries.seriesTeamTwoFinalScore])
                        }
                        r[++j] = '<div class="row" style="height: 100%">'
                        r[++j] = '<div class="card-panel horizontal matchRow center-align ';
                        r[++j] = teamOneBasic + teamTwoBasic;
                        r[++j] = '" id="match';
                         r[++j] = thisSeries.seriesId;
                        r[++j] = '"><span class="teamOne col s4 ';
                        r[++j] = teamOneBasic;
                        r[++j] = '"><strong class="vcenterText">';
                        r[++j] = '<img class="teamIcon" src="/static/images/dota/teams/';
                        r[++j] = teamOneBasic;
                        r[++j] = '.png"/>';
                        r[++j] = thisSeries.teamOne;
                        r[++j] = '</strong></span>';
                        r[++j] = '<div style="width: 180px;background-color: black;" class="card-panel horizontal predictionRow col s4 ';
                        r[++j] = thisSeries.started ? ' disabled" ' : ' active" ';
                        r[++j] = 'data-seriesId=';
                        r[++j] = thisSeries.seriesId;
                        r[++j] = '><strong><input class="col s5 center scoreboardfont" style="-moz-appearance: textfield" ';
                        r[++j] = thisSeries.started ? ' disabled=true' : "";
                        r[++j] = '  type="number" id="teamOneScorePredict-';
                        r[++j] = thisSeries.seriesId;
                        r[++j] = '">';
                        r[++j] = '<input style="color:#ff9900" class="col s2 center scoreboardfont" type="text" value=":" disabled><input class="col s5 center scoreboardfont" style="-moz-appearance: textfield" ';
                        r[++j] = thisSeries.started ? ' disabled=true' : "";
                        r[++j] = ' type="number" id="teamTwoScorePredict-';
                        r[++j] = thisSeries.seriesId;
                        r[++j] = '"></strong>';
                        r[++j] = '</div>';
                        r[++j] = '<span class="teamTwo col s4 right ';
                        r[++j] = teamTwoBasic;
                        r[++j] = '"><strong class="vcenterText">';
                        r[++j] = thisSeries.teamTwo;
                        r[++j] = '<img class="teamIcon" src="/static/images/dota/teams/';
                        r[++j] = teamTwoBasic;
                        r[++j] = '.png"/>';
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
                        var teamOneScorePredict = $("#teamOneScorePredict-" + entry.seriesId);
                        var teamTwoScorePredict = $("#teamTwoScorePredict-" + entry.seriesId);
                        var scores = matchIdToScores.get(entry.seriesId);
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
        if (inputs[0].value && inputs[2].value){
        data.predictions.push({
                    'seriesId': parseInt(elem.attr("data-seriesId")), "teamOneScore": inputs[0].valueAsNumber,
                     "teamTwoScore": inputs[2].valueAsNumber
                    });
            }
    })
    $.ajax({url: "/prediction_proxy",
                    type: "POST",
                    dataType: "json",
                    data: JSON.stringify(data),
                    contentType: "application/json",
                    success: function(){Swal.fire({
             title: "Success",
              type: "success",
              timer: 500
            })},
                    error: function(jqxhr, textStatus, errorThrown){
            Swal.fire({'text': jqxhr.responseText, 'type': 'error'});
        }
            });
}
$("#predictBtn").click(userId === null ? pleaseLogInClick : updatePredictions);
