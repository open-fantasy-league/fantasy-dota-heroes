var userCanTransfer
var teamUrl = apiBaseUrl + "leagues/" + leagueId + "/users/" + userId + "?team&scheduledTransfers&stats"
console.log(teamUrl)
var heroes;
$.ajax({url: apiBaseUrl + "pickees/league/" + leagueId + "/stats/",
            type: "GET",
            dataType: "json",
            success: function(data){
                userCanTransfer = (data.transferScheduled == null);
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
                r[++j] = '"><td class="heroImg" sorttable_customkey="';
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
                if (userCanTransfer){
                    r[++j] = '<button type="submit" name="buyHero" class="btn waves-effect waves-light" data-heroId="';
                    r[++j] = id;
                    r[++j] = '">Buy</button>';
                }
                r[++j] = '</td></tr>';
                })
                console.log(r.join(''))
                $("#heroesTable").find("tbody").html(r.join(''));
            },
            failure: function(data){
                sweetAlert("Something went wrong. oops!", '', 'error');
            }
        }).then(getTeam())
function getTeam(){
    $.ajax({url: teamUrl,
            dataType: "json",
            type: "GET",
            success: function(data){
                userCanTransfer = (data.leagueUser.transferScheduledTime == null);
                var r = new Array(), j = -1;
                $.each(data.team, function(key, hero) {
                    var id = hero.externalId;
                    console.log(heroes)
                    console.log(id)
                    var heroInfo = heroes.find(function(h){return h.externalId == id})
                    var imgSrc = "/static/images/dota/" + hero.name.replace(" ", "_") + "_icon.png";
                    var transferSymbol;
                    var transferClass = '';
                    if (data.scheduledTransfers.filter(function(t){return t.isBuy && t.externalId == id})){
                        transferSymbol = '<i class="material-icons">add_circle</i>'
                        transferClass = "toTransfer transferIn"
                    }
                    else if (data.scheduledTransfers.filter(function(t){return !t.isBuy && t.externalId == id})){
                        transferSymbol = '<i class="material-icons">remove_circle</i>'
                        transferClass = "toTransfer transferOut"
                    }
                r[++j] = '<tr class="teamRow ';
                r[++j] = transferClass;
                r[++j] = '" id="';
                r[++j] = id;
                r[++j] = '"><td class="heroImg" sorttable_customkey="';
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
                if (userCanTransfer){
                    r[++j] = '<button type="submit" name="sellHero" class="btn waves-effect waves-light" data-heroId="';
                    r[++j] = hero.id;
                    r[++j] = '">Sell</button>';
                }
                r[++j] = '</td></tr>';
                })
                $("#teamTable").find("tbody").html(r.join(''));
            },
            failure: function(data){
                sweetAlert("Something went wrong. oops!", '', 'error');
            }
        });
        }
/*
% for hero in heroes:
                <tr id="${hero.id}Row">
                    <td class="heroImg" sorttable_customkey="${hero.name}"><img src="/static/images/dota/${hero.name.replace(" ", "_")}_icon.png" title="${hero.name}"/></td>
                    <td class="heroEntry">${hero.name}</td>
                    <td class="heroPointsEntry">${hero.points}</td>
                    <td class="picksEntry extra">${hero.picks}</td>
                    <td class="bansEntry extra">${hero.bans}</td>
                    <td class="winsEntry extra">${hero.wins}</td>
                    <td class="valueEntry">${hero.value}</td>
                    <td class="tradeEntry">
                        <form name="tradeForm" id="${hero.id}TradeForm" class="tradeForm" onsubmit="return false;">
                            <input type="hidden" value="${hero.id}" name="tradeHero"/>
                            <button type="submit" name="buyHero" class="btn waves-effect waves-light">Buy</button>
                        </form>
                    </td>
                </tr>
            % endfor
*/