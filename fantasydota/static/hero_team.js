var teamUrl;
var heroes;
var tableContainer = $("#tableContainer");
var gridContainer = $("#gridContainer");
var showingActive = false;
signup();
getLeagueInfo().then(getPickees);

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
                    $.each(data.sort(function(a, b){return b.price - a.price}), function(key, hero) {
                        var id = hero.id;
                        var imgSrc = "/static/images/dota/" + hero.name.replace(/ /g, "_") + "_icon.png";
                        var pickImgSrc = "/static/images/dota/big/" + hero.name.toLowerCase().replace(/ /g, "_") + ".png";
                        //var pickImgSrc = "http://cdn.dota2.com/apps/dota2/images/heroes/" + hero.name.toLowerCase() + "_sb.png";
                        //console.log(pickImgSrc)
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
                        r[++j] = 'Row"><td class="tradeEntry">';
                        r[++j] = '<button type="submit" name="buyHero" class="btn waves-effect waves-light tableHeroBtn" disabled="true" data-heroId="';
                        r[++j] = id;
                        r[++j] = '">Buy</button></td><td class="heroImg" sorttable_customkey="';
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
                        r[++j] = '</td></tr>';
                    })
                    r2[++j2] = '</tr>';
                    $("#heroesTable").find("tbody").html(r.join(''));
                    $("#heroesTableGrid").find("tbody").html(r2.join(''));
                },
                error: function(data){
                    Swal.fire("Something went wrong. oops!", '', 'error');
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
        teamUrl = apiBaseUrl + "leagues/" + leagueId + "/users/" + userId + "?team&scheduledTransfers&stats&periods=";
        if (league.currentPeriod){
            teamUrl = teamUrl + league.currentPeriod.value.toString() + "," + (league.currentPeriod.value +1).toString();
            }
        else{
            teamUrl = teamUrl + "1";
            $("#activeTeamSwitchDiv").addClass('hide');
        }
        $.ajax({url: teamUrl,
                dataType: "json",
                type: "GET",
                success: function(data){
                    if (league.currentPeriod){
                        var futureTeam = data.team.find((t) => t.period == league.currentPeriod.value + 1).team;
                        var activeTeam = data.team.find((t) => t.period == league.currentPeriod.value).team;
                        }
                        else{
                        var futureTeam = data.team.find((t) => t.period == 1).team;
                        var activeTeam = futureTeam;
                        }
                    if (data.user.remainingTransfers != null && league.started){
                        $("#remainingTransfersSection").removeClass('hide');
                        $("#remainingTransfers").text(data.user.remainingTransfers);
                    }
                    $(".userCredits").text(data.user.money);
                    $(".userPoints").text(data.stats.points);
                    if (!league.started){
                        $("#infinityTransfersUntilStartMessage").removeClass('hide');
                    }
                    else{
                        $("#transferDelayMessage").removeClass('hide');
                    }
                    if (!data.user.usedWildcard && league.started){
                        $("#useWildcard").removeClass('hide');
                    }
                    var r = new Array(), j = -1;
                    $.each(futureTeam, function(key, hero) {
                        var id = hero.id;
                        var heroInfo = heroes.find(function(h){return h.id == id});
                        var imgSrc = "/static/images/dota/" + hero.name.replace(/ /g, "_") + "_icon.png";
                    r[++j] = '<tr class="teamRow ';
                        r[++j] = ' future';
                    r[++j] = '" id="future';
                    r[++j] = id;
                    r[++j] = 'TeamRow"><td class="tradeEntry">';
                    r[++j] = '<button type="submit" name="sellHero" class="btn waves-effect waves-light" disabled="true" data-heroId="';
                    r[++j] = id;
                    r[++j] = '">Sell</button><td class="heroImg" sorttable_customkey="';
                    r[++j] = hero.name;
                    r[++j] = '"><img src="';
                    r[++j] = imgSrc;
                    r[++j] = '" title="';
                    r[++j] = hero.name;
                    r[++j] = '"/></td><td class="heroEntry">';
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
                    r[++j] = '</td></tr>';
                    });
                    $.each(activeTeam, function(key, hero) {
                        var id = hero.id;
                        var heroInfo = heroes.find(function(h){return h.id == id});
                        var imgSrc = "/static/images/dota/" + hero.name.replace(/ /g, "_") + "_icon.png";
                    r[++j] = '<tr class="activex hide teamRow ';
                    r[++j] = '" id="';
                    r[++j] = id;
                    r[++j] = 'TeamRow"><td class="tradeEntry">';
                    r[++j] = '<button type="submit" name="sellHero" class="btn waves-effect waves-light" disabled="true" data-heroId="';
                    r[++j] = id;
                    r[++j] = '">Sell</button><td class="heroImg" sorttable_customkey="';
                    r[++j] = hero.name;
                    r[++j] = '"><img src="';
                    r[++j] = imgSrc;
                    r[++j] = '" title="';
                    r[++j] = hero.name;
                    r[++j] = '"/></td><td class="heroEntry">';
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
                    r[++j] = '</td></tr>';
                    });
                    $("#teamTable").find("tbody").html(r.join(''));
                },
                error: function(jqxhr, textStatus, errorThrown){
                        Swal.fire("Something went wrong. oops!", '', 'error');
                }
            }).then(setup);
        }
}

function setup(){
    league.transferOpen ? undisableButtons() : disableButtons();
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
                Swal.fire({
                 title: "Transfers locked in!",
                 text: league.started ? "Note: Your new heroes will start scoring points tomorrow" : "You can make as many changes as you like until league start",
                  type: "success"
                }).then(function(){
                    window.location.reload(false);
                });
            },
            error: function(jqxhr, textStatus, errorThrown){
                undisableButtons();
                Swal.fire(jqxhr.responseText, '', 'error');
            }
        });
    });

    $('#useWildcard').click(function() {
        var toSellOriginal = toSell.slice();
        var toBuyOriginal = toBuy.slice();
        disableButtons();
        if (toSell.length > 0){
            Swal.fire('Cannot use wildcard and sell heroes at same time', '', 'error');
        }
        $.ajax({
            url: '/transfer_proxy',
            dataType: "json",
            type: "POST",
            data: {"sell": toSell, "buy": toBuy, "isCheck": true, "wildcard": true},
            success: function(data){
                Swal.fire({
                type: 'warning',
                 title: "Are you sure you want to use wildcard?",
                 showCancelButton: true,
                 text: "(only available once)",
                }).then(function(result){
                    if (result.value){
                        wildcard = true;
                        $(".userCredits").each(function(){$(this).text(data.updatedMoney)});
                        $("[id$=TeamRow]").remove();
                        Swal.fire({
                         title: "Money refunded and team reset. Pick a new team and remember to confirm",
                         text: "(reload page to roll-back wildcard)",
                          type: "success"
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
                Swal.fire(jqxhr.responseText, '', 'error');
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
