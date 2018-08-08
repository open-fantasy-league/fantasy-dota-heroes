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

<%def name="getTransferStatus(teamHero)">
    % if not teamHero.active:
        toTransfer transferIn
    % elif teamHero.reserve:
        toTransfer transferOut
    % endif
</%def>

<%def name="getTransferSymbol(teamHero)">
    % if not teamHero.active:
        <i class="material-icons">add_circle</i>
    % elif teamHero.reserve:
        <i class="material-icons">remove_circle</i>
    % endif
</%def>

<div class="row" id="myTeamBlock">
    <span class="left"><h2>Team</h2></span>
    <span class="right"><h2>Points: <span class="teamPoints">${userq.points}</span></h2></span>
    <div id="tableContainer">
        <table class="sortable card-table striped centered" id="teamTable">
            <tr style="cursor: pointer">
                <th class="heroHeader">Hero</th>
                <th class="dummyHeader" colspan="0"></th>
                <th class="heroPointsHeader">Points</th>
                <th class="picksHeader extra">Picks</th>
                <th class="bansHeader extra">Bans</th>
                <th class="winsHeader extra">Wins</th>
                <th class="valueHeader">Value</th>
                <th class="sellHeader">Sell</th>

            </tr>
            % for hero in team:
                <tr class="teamRow ${getTransferStatus(hero[1])}" id="${hero[0].id}TeamRow">
                    <td class="heroImg" sorttable_customkey="${hero[0].name}"><img src="/static/images/dota/${hero[0].name.replace(" ", "_")}_icon.png" title="${hero[0].name}"/></td>
                    <td class="heroEntry">${getTransferSymbol(hero[1])}${hero[0].name}</td>
                    <td class="heroPointsEntry">${hero[0].points}</td>
                    <td class="picksEntry extra">${hero[0].picks}</td>
                    <td class="bansEntry extra">${hero[0].bans}</td>
                    <td class="winsEntry extra">${hero[0].wins}</td>
                    <td class="valueEntry">${hero[0].value}</td>
                    <td class="tradeEntry">
                        <form name="tradeForm" id="${hero[0].id}TradeForm" class="tradeForm" onsubmit="return false;">
                            <input type="hidden" value="${hero[0].id}" name="tradeHero"/>
                            % if hero[1].reserve == hero[1].active:
                                <button type="submit" name="${"buyHero" if hero[1].reserve else "sellHero"}" class="btn waves-effect waves-light" data-cancel=data-cancel>Cancel</button>
                            % else:
                                <button type="submit" name="sellHero" class="btn waves-effect waves-light">Sell</button>
                            % endif
                        </form>
                    </td>
                </tr>
            % endfor
        </table>
    </div>

    % if league.status > 0:
            <span class="right"><button type="submit" id="confirmTransfers" class="btn waves-effect waves-light">${'Confirm Team!' if not userq.swap_tstamp else 'Pending Transfers'}</button></span>
    % endif
</div>

<div class="card row">
    <div class="card-content">
        <p>50 Credits to pick a team of 5 heroes (Points penalties for under 5)</p>
        % if league.status > 0:
            You have ${userq.remaining_transfers} remaining available transfers (Transfers will not count until 'Confirm Transfers' pressed)
            % if not userq.swap_tstamp:
                <p><strong>
                    There is a 1 hour delay between confirmation of transfers and their processing (to prevent cheating/unfair advantages).
                </strong></p>
                <p>Further transfers are disabled during this hour period,
                however your old team does continue scoring points until transfers processed</p>
            % else:
                <span class="messageTransClosed"><p><strong>
                    Due to recent changes you are in transfer cooldown for ${int(time_until_swap[0])} hours, ${int(time_until_swap[1])} minutes.
                </strong></p></span>
            % endif
        % else:
            Once the tournament starts you will have 10 extra transfers you can make (You can make infinity changes before first game)
        % endif
        <p><strong><a href="/rules">Detailed Rules</a></strong></p>
        <span>
            <p>Tables are sortable (click table headers)</p>
        </span>
    </div>
</div>
<div id="heroesBlock" class="row">
    <h2>Heroes (Credits Available: <span class="userCredits">${round(userq.money, 1)}</span>)</h2>
    <div id="tableContainer">
        <table class="sortable card-table striped centered">
            <tr style="cursor: pointer">
                <th class="heroHeader">Hero</th>
                <th class="dummyHeader" colspan="0"></th>
                <th class="heroPointsHeader">Points</th>
                <th class="picksHeader extra">Picks</th>
                <th class="bansHeader extra">Bans</th>
                <th class="winsHeader extra">Wins</th>
                <th class="valueHeader">Value</th>
                <th class="sellHeader">Buy</th>
            </tr>
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
        </table>
    </div>
</div>

<script>
var leagueStarted = ${'true' if league.status > 0 else 'false'};
var league_id = ${league.id};
var transferCooldown = ${'true' if userq.swap_tstamp else 'false'};
var remainingTransfers = ${userq.remaining_transfers};
</script>

<script src="/static/trade.js"></script>
