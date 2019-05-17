var userCanTransfer;
var teamUrl;
var players;
var tableContainer = $("#tableContainer");
var gridContainer = $("#gridContainer");
var playerDataCache = new Map()
signup()
getLeagueInfo().then(getCards)

function signup(){
if (!apiRegistered){
                $.ajax({url: apiBaseUrl + "users/" + userId + "/join/" + leagueId + "?username=" + username,
                    dataType: "json",
                    type: "POST",
                    data: {"username": username, "userId": userId},
                    success: function(data){
                        console.log("signed up")
                    }
                })
            }
            }
//$.ajax({url: apiBaseUrl + "leagues/" + leagueId,
//    dataType: "json",
//    type: "GET",
//    success: function(data){
//        league = data;
//        console.log(league)
//    }
//}).then(getPickees)

function getCards(){
var nextPeriodValue = league.currentPeriod ? league.currentPeriod + 1: 1
var nextPeriodStart = league.periods[nextPeriodValue - 1].start
teamUrl = apiBaseUrl + "leagues/" + leagueId + "/users/" + userId + "?team&stats&time=" + nextPeriodStart;
    $("#leagueLink").attr('href', league.url);
    $("#leagueLink").text(league.name);
    $.ajax({url: apiBaseUrl + "teams/league/" + leagueId + "/user/" + userId + "/cards?time=" + nextPeriodStart,
                type: "GET",
                dataType: "json",
                success: function(data){
                    $.each(["Goalkeeper", "Defender", "Midfielder", "Forward"], function(key, position){
                        var positionLowerCase = position.toLowerCase()
                        var positionDiv = $("#" + positionLowerCase);
                        var p = [], j = -1;
                        $.each(data.filter(function(e){return e.limitTypes.position == position}), function(i, player) {
                            console.log(player)
                            playerDataCache.set(player.cardId, player);
                            p[++j] = '<div style="height: 400px;" class="card col s3 playerCard rounded rarity-';
                            p[++j] = player.colour.toLowerCase();
                            p[++j] = ' ';
                            p[++j] = player.limitTypes.club.split(" ").join("").toLowerCase();
                            p[++j] = '"><div class="card-content"><span class="card-title"><h6><p><span class="centre"><strong>';
                            p[++j] = player.name;
                            p[++j] = '</strong></span></p><p><span class="centre">';
                            p[++j] = player.limitTypes.club;
                            p[++j] = '</span></p></h6></span><p><span class="left">';
                            p[++j] = player.limitTypes.position;
                            p[++j] = '</span><span class="right"><button name="buyPlayer" id="addTeam-';
                            p[++j] = player.cardId;
                            p[++j] = '" type="submit" class="btn waves-effect waves-light addTeam" data-cardId="';
                            p[++j] = player.cardId;
                            p[++j] ='">Add</button></span></p>';
                            p[++j] = '</p><div class="card-image"><img src="/static/images/football/placeholder.png"></div><p>';
                            $.each(player.bonuses, function(bkey, bonus){
                                console.log(bonus)
                                p[++j] = '<p><strong><span>→';
                                p[++j] = bonus.name;
                                p[++j] = ' x';
                                p[++j] = bonus.multiplier;
                                p[++j] = '</span></strong></p>';
                            })
                            p[++j] = '<span class="centre"><button name="recyclePlayer" id="recyclePlayer-';
                            p[++j] = player.cardId;
                            p[++j] = '" type="submit" class="btn waves-effect waves-light recyclePlayer" data-cardId="';
                            p[++j] = player.cardId;
                            p[++j] ='">Recycle</button></span>';
                            p[++j] = '</p></div></div>';
                        })
                    $("#" + positionLowerCase + "s").html(p.join(''));
                    })
                },
                error: function(data){
                    sweetAlert("Something went wrong. oops!", '', 'error');
                }
            }).then(getTeamThenSetup);
            }

function addPlayerHtmlArray(player, r, j){
                    r[++j] = '<tr class="teamRow ';
                    r[++j] = 'toSell';
                    r[++j] = '" id="';
                    r[++j] = player.cardId;
                    r[++j] = 'TeamRow"><td class="playerImg" sorttable_customkey="';
                    r[++j] = player.name;
                    r[++j] = '">';
                    r[++j] = '</td><td class="playerEntry"><strong>';
                    r[++j] = player.name;
                    r[++j] = '</strong></td><td class="positionEntry">';
                    r[++j] = player.limitTypes.position;
                    r[++j] = '</td><td class="clubEntry">';
                    r[++j] = player.limitTypes.club;
                    r[++j] = '</td><td class="playerPointsEntry">';
                    r[++j] = 2.1;
                    //r[++j] = player.stats.points;
                    r[++j] = '</td><td class="bonusesEntry">';
                    $.each(player.bonuses, function(bkey, bonus){
                        r[++j] = '<p><span>→';
                                r[++j] = bonus.name;
                                r[++j] = ' x';
                                r[++j] = bonus.multiplier;
                                r[++j] = '</span></p>';
                    })
                    r[++j] = '</td><td class="tradeEntry">';
                    r[++j] = '<button type="submit" name="sellPlayer" class="btn waves-effect waves-light" disabled="true" data-cardId="';
                    r[++j] = player.cardId;
                    r[++j] = '">Remove</button>';
                    r[++j] = '</td></tr>';
        return r, j
}

function getTeamThenSetup(){
    if (userId == null){
        $("#pleaseLogIn").css('display', 'initial');
        undisableButtons();
        $('button[name=buyPlayer]').each(function (key, btn){
            $(this).click(pleaseLogInClick);
        });
        $('#confirmTransfers').click(pleaseLogInClick);
    }
    else{
        $.ajax({url: teamUrl,
                dataType: "json",
                type: "GET",
                success: function(data){
                    userCanTransfer = (league.transferOpen);
                    $(".userCredits").text(data.user.money);
                    $(".userPoints").text(data.stats.points);
                    var r = new Array(), j = -1;
                    $.each(data.team, function(key, player) {
                    r, j = addPlayerHtmlArray(player, r, j);
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
    $('ul.tabs').tabs();
    undisableButtons();
    $('button[name=buyPlayer]').add('button[name=sellPlayer]').each(function (key, btn){
        $(this).click(tradeOnclick);
    });

    $('.recyclePlayer').each(function (key, btn){
        $(this).click(recycleOnClick);
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
                 text: league.started ? "Note: Your new players will start scoring points one hour from now" : "You can make as many changes as you like until league start",
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

    $('#newCardPack').click(function() {
        $.ajax({
            url: "/new_card_pack",
            dataType: "json",
            type: "GET",
            success: function(data){
                    window.location.reload(false);
            },
            error: function(jqxhr, textStatus, errorThrown){
                sweetAlert(jqxhr.responseText, '', 'error');
            }
        });
    })
}