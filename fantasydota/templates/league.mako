<%inherit file="layout.mako"/>

<%def name="title()">
    League Team: ${league.name}
</%def>

<%def name="meta_keywords()">
    League, Dota, fantasy, points, game
</%def>

<%def name="meta_description()">
    League page for fantasy dota game.
</%def>

<%def name="checkPositiveBuy(cost, value)">
    % if cost < value:
        positive
    % elif cost == value:
        neutral
    % else:
        negative
    % endif
</%def>

<div class="row" id="myTeamBlock">
    <h2>My Team (Total points <span class="teamPoints">${userq.points}</span>)</h2>
    <div id="tableContainer">
        <table class="sortable responsive-table card-table striped centered" id="teamTable">
            <tr style="cursor: pointer">
                <th class="heroHeader">Hero</th>
                <th class="dummyHeader" colspan="0"></th>
                <th class="heroPointsHeader">Points</th>
                <th class="picksHeader">Picks</th>
                <th class="bansHeader">Bans</th>
                <th class="winsHeader">Wins</th>
                <th class="valueHeader">Current value</th>
                <th class="costHeader">Paid</th>
                <th class="sellHeader">Sell</th>

            </tr>
            % for hero in team:
                <tr class="teamRow" id="${hero[0].id}TeamRow">
                    <td class="heroImg" sorttable_customkey="${hero[0].name}"><img src="/static/images/${hero[0].name.replace(" ", "_")}_icon.png" title="${hero[0].name}"/></td>
                    <td class="heroEntry">${hero[0].name}</td>
                    <td class="heroPointsEntry">${hero[0].points}</td>
                    <td class="picksEntry">${hero[0].picks}</td>
                    <td class="bansEntry">${hero[0].bans}</td>
                    <td class="winsEntry">${hero[0].wins}</td>
                    <td class="valueEntry">${hero[0].value}</td>
                    <td class="costEntry ${checkPositiveBuy(hero[1].cost, hero[0].value)}">${hero[1].cost}</td>
                    <td class="tradeEntry">
                        <form name="tradeForm" id="${hero[0].id}TradeForm" class="tradeForm" onsubmit="return false;">
                            <input type="hidden" value="${hero[0].id}" name="tradeHero"/>
                            <button type="submit" name="sellHero" class="btn waves-effect waves-light">Sell</button>
                        </form>
                    </td>
                </tr>
            % endfor
        </table>
    </div>
</div>
<div class="card row">
    <div class="card-content">
        <span class=${"messageTransOpen" if league.transfer_open != 0 else "messageTransClosed"}>
            <p><strong>${"Transfer window currently open. Closes ~1 hour before games start." if league.transfer_open != 0 else """Transfer window closed until todays games end"""}
            </strong></p>
        </span>
        <span>
            <p>Tables are sortable (click table headers). Max <strong>5 heroes per team</strong> (points <a href="/rules">penalties</a> for under 5)</p>
        </span>
    </div>
</div>
<div id="heroesBlock" class="row">
    <h2>Heroes (Credits Available: <span class="userCredits">${round(userq.money, 1)}</span>)</h2>
    <div id="tableContainer">
        <table class="sortable responsive-table card-table striped centered">
            <tr>
                <th class="heroHeader">Hero</th>
                <th class="dummyHeader" colspan="0"></th>
                <th class="heroPointsHeader">Points</th>
                <th class="picksHeader">Picks</th>
                <th class="bansHeader">Bans</th>
                <th class="winsHeader">Wins</th>
                <th class="valueHeader">Value</th>
                <th class="sellHeader">Buy</th>
            </tr>
            % for hero in heroes:
                <tr id="${hero.id}Row">
                    <td class="heroImg" sorttable_customkey="${hero.name}"><img src="/static/images/${hero.name.replace(" ", "_")}_icon.png" title="${hero.name}"/></td>
                    <td class="heroEntry">${hero.name}</td>
                    <td class="heroPointsEntry">${hero.points}</td>
                    <td class="picksEntry">${hero.picks}</td>
                    <td class="bansEntry">${hero.bans}</td>
                    <td class="winsEntry">${hero.wins}</td>
                    <td class="valueEntry">${hero.value}</td>
                    <td class="tradeEntry">
                        <form name="tradeForm" id="${hero.id}TradeForm" class="tradeForm" onsubmit="return false;">
                            <input type="hidden" value="${hero.id}" name="tradeHero"/>
                            <button type="submit" name="buyHero" class="btn waves-effect waves-light">Buy</button>
                        </form>
                    </td>
                </tr>
            % endfor
        </table>
    </div>
</div>


<script>
var transfers = ${'true' if league.transfer_open != 0 else 'false'};
var league_id = ${league.id};
</script>

<script src="/static/trade.js"></script>
