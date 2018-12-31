var userCanTransfer;
var teamUrl = apiBaseUrl + "leagues/" + leagueId + "/users/" + userId + "?team&scheduledTransfers&stats";
console.log(teamUrl)
var heroes;
$.ajax({url: apiBaseUrl + "pickees/leagues/" + leagueId + "/stats/",
            type: "GET",
            dataType: "json",
            success: function(data){
                var r = new Array(), j = -1;
                heroes = data;
                $.each(data, function(key, hero) {
                    teamTableHeader.appendAfter
                    var id = hero.externalId;
                    var imgSrc = "/static/images/dota/" + hero.name.replace(" ", "_") + "_icon.png";
                r[++j] = '<tr class="';
                r[++j] = id;
                r[++j] = 'Row';
                r[++j] = '" id="';
                r[++j] = id;
                r[++j] = 'Row"><td class="heroImg" sorttable_customkey="';
                r[++j] = hero.name;
                r[++j] = '"><img src="';
                r[++j] = imgSrc;
                r[++j] = '" title="';
                r[++j] = hero.name;
                r[++j] = '"/></td><td class="heroEntry">';
                r[++j] = hero.name;
                r[++j] = '</td><td class="heroPointsEntry">';
                r[++j] = hero.stats.points;
                r[++j] = '</td><td class="picksEntry extra">';
                r[++j] = hero.stats.picks;
                r[++j] = '</td><td class="bansEntry extra">';
                r[++j] = hero.stats.bans;
                r[++j] = '</td><td class="winsEntry extra">';
                r[++j] = hero.stats.wins;
                r[++j] = '</td><td class="valueEntry">';
                r[++j] = hero.cost;
                r[++j] = '</td><td class="tradeEntry">';
                r[++j] = '<button type="submit" name="buyHero" class="btn waves-effect waves-light" disabled="true" data-heroId="';
                r[++j] = id;
                r[++j] = '">Buy</button>';
                r[++j] = '</td></tr>';
                })
                console.log(r.join(''))
                $("#heroesTable").find("tbody").html(r.join(''));
            },
            failure: function(data){
                sweetAlert("Something went wrong. oops!", '', 'error');
            }
        }).then(getTeamThenSetup)

function getTeamThenSetup(){
    $.ajax({url: teamUrl,
            dataType: "json",
            type: "GET",
            success: function(data){
                userCanTransfer = (league.transferOpen && data.leagueUser.transferScheduledTime == null);
                console.log("usercanTransfer:" + userCanTransfer);
                $("#remainingTransfers").text(data.leagueUser.remainingTransfers);
                $(".userCredits").text(data.leagueUser.money);
                $(".userPoints").text(data.leagueUser.stats.points);
                if (data.leagueUser.changeTstamp){
                    $("#messageTransferCooldown").style('visible', 'default');
                }
                if (!league.started){
                    $("#infinityTransfersUntilStartMessage").style('visible', 'default');
                }
                var r = new Array(), j = -1;
                $.each(data.team, function(key, hero) {
                    var id = hero.externalId;
                    console.log(hero)
                    console.log(id)
                    var heroInfo = heroes.find(function(h){return h.externalId == id})
                    var imgSrc = "/static/images/dota/" + hero.name.replace(" ", "_") + "_icon.png";
                    var transferSymbol;
                    var transferClass = '';
                    if (data.scheduledTransfers.includes(function(t){return t.isBuy && t.externalId == id})){
                        transferSymbol = '<i class="material-icons">add_circle</i>'
                        transferClass = "toTransfer transferIn"
                    }
                    else if (data.scheduledTransfers.includes(function(t){return !t.isBuy && t.externalId == id})){
                        transferSymbol = '<i class="material-icons">remove_circle</i>'
                        transferClass = "toTransfer transferOut"
                    }
                r[++j] = '<tr class="teamRow ';
                r[++j] = transferClass;
                r[++j] = '" id="';
                r[++j] = id;
                r[++j] = 'TeamRow"><td class="heroImg" sorttable_customkey="';
                r[++j] = hero.name;
                r[++j] = '"><img src="';
                r[++j] = imgSrc;
                r[++j] = '" title="';
                r[++j] = hero.name;
                r[++j] = '"/></td><td class="heroEntry">';
                r[++j] = transferSymbol;
                r[++j] = hero.name;
                r[++j] = '</td><td class="heroPointsEntry">';
                r[++j] = heroInfo.stats.points;
                r[++j] = '</td><td class="picksEntry extra">';
                r[++j] = heroInfo.stats.picks;
                r[++j] = '</td><td class="bansEntry extra">';
                r[++j] = heroInfo.stats.bans;
                r[++j] = '</td><td class="winsEntry extra">';
                r[++j] = heroInfo.stats.wins;
                r[++j] = '</td><td class="valueEntry">';
                r[++j] = hero.cost;
                r[++j] = '</td><td class="tradeEntry">';
                r[++j] = '<button type="submit" name="sellHero" class="btn waves-effect waves-light" disabled="true" data-heroId="';
                r[++j] = id;
                r[++j] = '">Sell</button>';
                r[++j] = '</td></tr>';
                })
                $("#teamTable").find("tbody").html(r.join(''));
            },
            failure: function(data){
                sweetAlert("Something went wrong. oops!", '', 'error');
            }
        }).then(setup);
}

function setup(){
    console.log(userCanTransfer)
    userCanTransfer ? undisableButtons() : disableButtons();
    $('button[name=buyHero]').add('button[name=sellHero]').each(function (key, btn){
        $(this).click(tradeOnclick);
    });

    $('#confirmTransfers').click(function() {
        disableButtons()
        $.ajax({
            url: apiBaseUrl + "transfers/leagues/" + leagueId + "/users/" + userId,
            dataType: "json",
            type: "POST",
            data: {"sell": toSell, "buy": toBuy, "isCheck": false},
            success: function(data){
                swal({
                 title: "Transfers locked in!",
                 text: "Note: Your new heroes will start scoring points one hour from now",
                  icon: "success"
                }).then(function(){
                    window.location.reload(false);
                });
            },
            error: function(jqxhr, textStatus, errorThrown){
                undisableButtons();
                sweetAlert(jqxhr.responseText, '', 'error');
            }
        });
    });
}

function setupInfoText(){

}