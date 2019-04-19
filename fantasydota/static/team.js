var userCanTransfer;
var teamUrl = apiBaseUrl + "leagues/" + leagueId + "/users/" + userId + "?team&scheduledTransfers&stats";
var heroes;
var tableContainer = $("#tableContainer");
var gridContainer = $("#gridContainer");
getLeagueInfo().then(getPickees)
//$.ajax({url: apiBaseUrl + "leagues/" + leagueId,
//    dataType: "json",
//    type: "GET",
//    success: function(data){
//        league = data;
//        console.log(league)
//    }
//}).then(getPickees)

function getPickees(){
    $("#leagueLink").attr('href', league.url);
    $("#leagueLink").text(league.name);
    $.ajax({url: apiBaseUrl + "pickees/leagues/" + leagueId + "/stats/",
                type: "GET",
                dataType: "json",
                success: function(data){
                    var r = new Array(), j = -1;
                    var r2 = new Array(), j2 = -1;
                    r2[++j2] = '<tr>';
                    heroes = data;
                    $.each(data, function(key, hero) {
                        var id = hero.id;
                        var imgSrc = "/static/images/dota/" + hero.name.replace(/ /g, "_") + "_icon.png";
                        var pickImgSrc = "/static/images/dota/big/" + hero.name.toLowerCase().replace(/ /g, "_") + ".png";
                        //var pickImgSrc = "http://cdn.dota2.com/apps/dota2/images/heroes/" + hero.name.toLowerCase() + "_sb.png";
                        console.log(pickImgSrc)
                        if (key % 8 == 0){
                            r2[++j2] = '</tr><tr>';
                        }
                        else if (key % 4 == 0){
                            r2[++j2] = '<td>&nbsp;&nbsp;&nbsp;&nbsp;</td>';
                        }
                        r2[++j2] = '<td title="';
                        r2[++j2] = hero.name;
                        r2[++j2] = '" style="background-image: url(';
                        r2[++j2] = pickImgSrc;
                        r2[++j2] = '); background-repeat: no-repeat; background-size: 100% 100%; width: 128px; height: 72px;">';
                        r2[++j2] = '<div class="gridHeroDiv"><button type="submit" name="buyHero" class="btn waves-effect waves-light gridHeroBtn" disabled="true" data-heroId="';
                        r2[++j2] = id;
                        r2[++j2] = '">';
                        r2[++j2] = hero.price;
                        r2[++j2] = '</button></div>';
                        r2[++j2] = '</td>';
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
                        r[++j] = hero.price;
                        r[++j] = '</td><td class="tradeEntry">';
                        r[++j] = '<button type="submit" name="buyHero" class="btn waves-effect waves-light tableHeroBtn" disabled="true" data-heroId="';
                        r[++j] = id;
                        r[++j] = '">Buy</button>';
                        r[++j] = '</td></tr>';
                    })
                    r2[++j2] = '</tr>';
                    $("#heroesTable").find("tbody").html(r.join(''));
                    $("#heroesTableGrid").find("tbody").html(r2.join(''));
                },
                error: function(data){
                    sweetAlert("Something went wrong. oops!", '', 'error');
                }
            }).then(getTeamThenSetup);
            }

function getTeamThenSetup(){
    if (userId == null){
        $("#pleaseLogIn").css('display', 'initial');
        undisableButtons();
        $('button[name=buyHero]').each(function (key, btn){
            $(this).click(pleaseLogInClick);
        });
        $('#confirmTransfers').click(pleaseLogInClick);
    }
    else{
        $.ajax({url: teamUrl,
                dataType: "json",
                type: "GET",
                success: function(data){
                    userCanTransfer = (league.transferOpen && data.leagueUser.transferScheduledTime == null);
                    if (data.leagueUser.remainingTransfers != null && league.started){
                        $("#remainingTransfersSection").css('display', 'initial');
                        $("#remainingTransfers").text(data.leagueUser.remainingTransfers);
                    }
                    $(".userCredits").text(data.leagueUser.money);
                    $(".userPoints").text(data.stats.points);
                    if (data.leagueUser.transferScheduledTime){
                        $("#messageTransferCooldown").css('display', 'initial');
                    }
                    if (!league.started){
                        $("#infinityTransfersUntilStartMessage").css('display', 'initial');
                    }
                    else{
                      $("#transferDelayMessage").css('display', 'initial');
                    }
                    if (!data.leagueUser.usedWildcard && league.started){
                        $("#useWildcard").css('display', 'initial');
                    }
                    var r = new Array(), j = -1;
                    $.each(data.scheduledTransfers, function(key, t){
                        if (t.isBuy) {
                            var buying = {'name': t.pickeeName, 'isBuy': true, 'id': t.pickeeId};
                            data.team.push(buying);
                        }
                    });
                    $.each(data.team, function(key, hero) {
                        var id = hero.id;
                        var heroInfo = heroes.find(function(h){return h.id == id})
                        var imgSrc = "/static/images/dota/" + hero.name.replace(/ /g, "_") + "_icon.png";
                        var transferSymbol;
                        var transferClass = '';
                        if (hero.isBuy){
                        //if (data.scheduledTransfers.includes(function(t){return t.isBuy && t.id == id})){
                            transferSymbol = '<i class="material-icons">add_circle</i>'
                            transferClass = "toTransfer transferIn"
                        }
                        else if (data.scheduledTransfers.includes(function(t){return !t.isBuy && t.id == id})){
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
                    r[++j] = hero.price;
                    r[++j] = '</td><td class="tradeEntry">';
                    r[++j] = '<button type="submit" name="sellHero" class="btn waves-effect waves-light" disabled="true" data-heroId="';
                    r[++j] = id;
                    r[++j] = '">Sell</button>';
                    r[++j] = '</td></tr>';
                    })
                    $("#teamTable").find("tbody").html(r.join(''));
                },
                error: function(jqxhr, textStatus, errorThrown){
                    if (jqxhr.responseText.startsWith("User does not exist on api")){
                        // need to add user first
                         $.ajax({url: apiBaseUrl + "users/",
                                dataType: "json",
                                type: "POST",
                                contentType: "application/json",
                                data: JSON.stringify({"username": username, "userId": userId}),
                                dataType: "json"
                                }).then(getTeamThenSetup)  // this time the call should work
                    }
                    else{
                        sweetAlert("Something went wrong. oops!", '', 'error');
                        }
                }
            }).then(setup);
        }
}

function setup(){
    userCanTransfer ? undisableButtons() : disableButtons();
    $('button[name=buyHero]').add('button[name=sellHero]').each(function (key, btn){
        $(this).click(tradeOnclick);
    });

    $('#confirmTransfers').click(function() {
        disableButtons()
        $.ajax({
            url: "/transfer_proxy",
            dataType: "json",
            type: "POST",
            data: {"sell": toSell, "buy": toBuy, "isCheck": false, "wildcard": wildcard},
            success: function(data){
                swal({
                 title: "Transfers locked in!",
                 text: league.started ? "Note: Your new heroes will start scoring points one hour from now" : "You can make as many changes as you like until league start",
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

    $('#useWildcard').click(function() {
        var toSellOriginal = toSell.slice();
        var toBuyOriginal = toBuy.slice();
        disableButtons();
        if (toSell.length > 0){
            sweetAlert('Cannot use wildcard and sell heroes at same time', '', 'error');
        }
        $.ajax({
            url: '/transfer_proxy',
            dataType: "json",
            type: "POST",
            data: {"sell": toSell, "buy": toBuy, "isCheck": true, "wildcard": true},
            success: function(data){
                swal({
                icon: 'warning',
                 title: "Are you sure you want to use wildcard?",
                 buttons: {cancel: true, confirm: true},
                 text: "(only available once)",
                }).then(function(result){
                    if (result){
                        wildcard = true;
                        $(".userCredits").each(function(){$(this).text(data.updatedMoney)});
                        $("[id$=TeamRow]").remove();
                        swal({
                         title: "Money refunded and team reset. Pick a new team and remember to confirm",
                         text: "(reload page to roll-back wildcard)",
                          icon: "success"
                        })
                        undisableButtons();
                    }
                    else{
                        wildcard = false;
                        toSell = toSellOriginal;
                        toBuy = toBuyOriginal;
                        undisableButtons();
                    }
                });
            },
            error: function(jqxhr, textStatus, errorThrown){
                toSell = toSellOriginal;
                toBuy = toBuyOriginal;
                undisableButtons();
                sweetAlert(jqxhr.responseText, '', 'error');
            }
        });
    });
}

function switchGridTable(inp){
    if (inp.checked != true){
        tableContainer.css('display', 'initial');
        gridContainer.css('display', 'none');
    }
    else{
        gridContainer.css('display', 'initial');
        tableContainer.css('display', 'none');
    }

}