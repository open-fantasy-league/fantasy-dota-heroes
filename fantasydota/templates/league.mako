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

<div>
    <nav>
    <div class="nav-wrapper">
        <ul class="left">
            <li class="active">
                <a href="/viewLeague?league=${league.id}"><b>Team</b></a>
            </li>
            <li>
                <a href="/leaderboard?league=${league.id}"><b>Leaderboard</b></a>
            </li>
        </ul>
    </div>
    </nav>
    <p>Hi ${username}</p>
    <span class=${"messageTransOpen" if league.transfer_open != 0 else "messageTransClosed"}>
        <p>${"Transfer window currently open. Closes ~1 hour before games start." if league.transfer_open == 0 else """Transfer window now closed for tournament. You can still change your battlecup team daily though."""}
        </p>
    </span>
    <span>
    <p>Tables are sortable (click table headers). Max 5 heroes per team (points <a href="/rules">penalties</a> for <5)</p>
    </span
</div>

<div id="myTeamBlock">
    <h2>My Team (Total points <span class="teamPoints">${userq.points}</span>)</h2>
    <div id="tableContainer">
        <table class="sortable" id="teamTable">
            <tr>
                <th class="heroHeader">Hero</th>
                <th class="heroPointsHeader">Points</th>
                <th class="picksHeader">Picks</th>
                <th class="bansHeader">Bans</th>
                <th class="winsHeader">Wins</th>
                <th class="valueHeader">Current value</th>
                <th class="costHeader">Loan cost</th>
                <th class="daysHeader">Days left</th>
                <th class="sellHeader">Cancel loan</th>

            </tr>
            % for hero in [hero_ for hero_ in team if hero_[1].active]:
                <tr class="teamRow" id="${hero[0].id}TeamRow">
                    <td class="heroEntry"><img src="/static/images/${hero[0].name.replace(" ", "_")}_icon.png"/>
                        ${hero[0].name}
                    </td>
                    <td class="heroPointsEntry">${hero[0].points}</td>
                    <td class="picksEntry">${hero[0].picks}</td>
                    <td class="bansEntry">${hero[0].bans}</td>
                    <td class="winsEntry">${hero[0].wins}</td>
                    <td class="valueEntry">${hero[0].value}</td>
                    <td class="costEntry">${hero[1].cost}</td>
                    <td class="daysEntry">${hero[1].days_left}</td>
                </tr>
            % endfor
        </table>

        <h4>Pending loan requests</h4>
        <table id="teamTableTransfers">
            % for hero in [hero_ for hero_ in team if not hero_[1].active]:
                <tr class="teamRow toBuy" id="${hero[0].id}TeamRow">
                    <td class="heroEntry"><img src="/static/images/${hero[0].name.replace(" ", "_")}_icon.png"/>
                        ${hero[0].name}
                    </td>
                    <td class="heroPointsEntry">${hero[0].points}</td>
                    <td class="picksEntry">${hero[0].picks}</td>
                    <td class="bansEntry">${hero[0].bans}</td>
                    <td class="winsEntry">${hero[0].wins}</td>
                    <td class="valueEntry">${hero[0].value}</td>
                    <td class="costEntry">${hero[1].cost}</td>
                    <td class="daysEntry">${hero[1].days_left}</td>
                    <td class="tradeEntry">
                        <form name="tradeForm" id="${hero[0].id}TradeForm" class="tradeForm" onsubmit="return false;">
                            <input type="hidden" value="${hero[0].id}" name="tradeHero"/>
                            <button type="submit" name="sellHero">Cancel loan</button>
                        </form>
                    </td>
                </tr>
            % endfor
        </table>
    </div>
    <h2>Heroes (Credits Available: <span class="userCredits">${round(50 - (sum([hero[0].value for hero in team])), 1)}</span>)</h2>
    <div id="tableContainer">
        <table class="sortable">
            <tr>
                <th class="heroHeader">Hero</th>
                <th class="heroPointsHeader">Points</th>
                <th class="picksHeader">Picks</th>
                <th class="bansHeader">Bans</th>
                <th class="winsHeader">Wins</th>
                <th class="valueHeader">Value</th>
                <th class="adjustedValueHeader">Loan cost</th>
                <th class="daysHeader">Days</th>
                <th class="sellHeader">Loan</th>

            </tr>
            % for hero in heroes:
                <tr id="${hero.id}Row">
                    <td class="heroEntry"><img src="/static/images/${hero.name.replace(" ", "_")}_icon.png"/>${hero.name}</td>
                    <td class="heroPointsEntry">${hero.points}</td>
                    <td class="picksEntry">${hero.picks}</td>
                    <td class="bansEntry">${hero.bans}</td>
                    <td class="winsEntry">${hero.wins}</td>
                    <td class="valueEntry">${hero.value}</td>
                    <td class="adjustedValueEntry">${hero.value}</td>
                    <td class="daysEntry"><input type="number" name="days" value=1 min=1 max=${league.days} /></td>
                    <td class="tradeEntry">
                        <form name="tradeForm" id="${hero.id}TradeForm" class="tradeForm" onsubmit="return false;">
                            <input type="hidden" value="${hero.id}" name="tradeHero"/>
                            <button type="submit" name="buyHero">Loan</button>
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
var mode = "league";

</script>

<script src="/static/trade.js"/>

