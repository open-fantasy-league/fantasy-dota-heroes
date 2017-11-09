<div class="row" id="myTeamBlock">
    <span class="left"><h2>My Team (Credits: <span class="userCredits">${round(userq.money, 1)}</span>)</h2></span>
    <span class="right"><h2>Total points: <span class="teamPoints">${userq.points}</span></h2></span>
    <div id="tableContainer">
        <table class="sortable responsive-table card-table striped centered" id="teamTable">
            <tr style="cursor: pointer">
                <th class="heroHeader">Hero</th>
                <th class="dummyHeader" colspan="0"></th>
                <th class="heroPointsHeader">Points</th>
                <th class="picksHeader">Picks</th>
                <th class="bansHeader">Bans</th>
                <th class="winsHeader">Wins</th>
                <th class="valueHeader">Value</th>
                <th class="sellHeader">${"Sell" if not league.swap_open else "Swap"}</th>

            </tr>
            % for hero in team:
                <tr class="teamRow" id="${hero[0].id}TeamRow">
                    <td class="heroImg" sorttable_customkey="${hero[0].name}"><img src="/static/images/dota/${hero[0].name.replace(" ", "_")}_icon.png" title="${hero[0].name}"/></td>
                    <td class="heroEntry">${hero[0].name}</td>
                    <td class="heroPointsEntry">${hero[0].points}</td>
                    <td class="picksEntry">${hero[0].picks}</td>
                    <td class="bansEntry">${hero[0].bans}</td>
                    <td class="winsEntry">${hero[0].wins}</td>
                    <td class="valueEntry">${hero[0].value}</td>
                    <td class="tradeEntry">
                        <form name="tradeForm" id="${hero[0].id}TradeForm" class="tradeForm" onsubmit="return false;">
                            <input type="hidden" value="${hero[0].id}" name="tradeHero"/>
                            <input type="hidden" value="0" name="tradeReserve"/>
                            <button type="submit" name=${"sellHero" if not league.swap_open else "swapOutHero"} class="btn waves-effect waves-light">${"Sell" if not league.swap_open else "Swap"}</button>
                        </form>
                    </td>
                </tr>
            % endfor
        </table>
    </div>
</div>

<div class="row" id="myReserveBlock">
    % if league.transfer_open:
        <span class="left"><h2>My Reserves (Credits: <span class="userReserveCredits">${round(userq.reserve_money, 1)}</span>)</h2></span>
    % else:
        <span class="left"><h2>My Reserves</h2></span>
    % endif
    <div id="tableContainer">
        <table class="sortable responsive-table card-table striped centered" id="reserveTable">
            <tr style="cursor: pointer">
                <th class="heroHeader">Hero</th>
                <th class="dummyHeader" colspan="0"></th>
                <th class="heroPointsHeader">Points</th>
                <th class="picksHeader">Picks</th>
                <th class="bansHeader">Bans</th>
                <th class="winsHeader">Wins</th>
                <th class="valueHeader">Value</th>
                <th class="sellHeader">${"Sell" if not league.swap_open else "Swap"}</th>
            </tr>
            % for hero in reserve_team:
                <tr class="reserveRow" id="${hero[0].id}ReserveRow">
                    <td class="heroImg" sorttable_customkey="${hero[0].name}"><img src="/static/images/dota/${hero[0].name.replace(" ", "_")}_icon.png" title="${hero[0].name}"/></td>
                    <td class="heroEntry">${hero[0].name}</td>
                    <td class="heroPointsEntry">${hero[0].points}</td>
                    <td class="picksEntry">${hero[0].picks}</td>
                    <td class="bansEntry">${hero[0].bans}</td>
                    <td class="winsEntry">${hero[0].wins}</td>
                    <td class="valueEntry">${hero[0].value}</td>
                    <td class="tradeEntry">
                        <form name="tradeForm" id="${hero[0].id}TradeForm" class="tradeForm" onsubmit="return false;">
                            <input type="hidden" value="${hero[0].id}" name="tradeHero"/>
                            <input type="hidden" value="1" name="tradeReserve"/>
                            <button type="submit" name=${"sellHero" if not league.swap_open else "swapInHero"} class="btn waves-effect waves-light">${"Sell" if not league.swap_open else "Swap"}</button>
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
            % if league.transfer_open != 0:
            <p><strong>NEW SYSTEM!</strong></p>
            <p>You are given <strong>100 credits total</strong> to pick both a <strong>Main team and Reserve team</strong></p>
            <p>Your <strong>Reserves score 0 points</strong>. However they can be <strong>swapped with main heroes each evening</strong> after games are over</p>
            <p>You <strong>cannot purchase any new heroes once tournament started</strong>. You must pick Main and Reserves carefully</p>
            <p><strong>Transfer window currently open (closes ~1 hour before games start)</strong></p>
            % else:
                <p><strong>
                Swaps between reserves and main team only available between days. When all day's games finished
                </strong></p>
            % endif
        </span>
        <span>
            <p>Tables are sortable (click table headers). Max <strong>5 heroes per team</strong> (points <a href="/rules">penalties</a> for under 5)</p>
        </span>
    </div>
</div>
<div id="heroesBlock" class="row">
    % if league.transfer_open:
        <h2>Heroes (Credits Available: <span class="userCredits">${round(userq.money, 1)}</span>, Reserve Credits: <span class="userReserveCredits">${round(userq.reserve_money, 1)}</span>)</h2>
    % else:
        <h2>Heroes</h2>
    % endif
    <div id="tableContainer">
        <table class="sortable responsive-table card-table striped centered">
            <tr style="cursor: pointer">
                <th class="heroHeader">Hero</th>
                <th class="dummyHeader" colspan="0"></th>
                <th class="heroPointsHeader">Points</th>
                <th class="picksHeader">Picks</th>
                <th class="bansHeader">Bans</th>
                <th class="winsHeader">Wins</th>
                <th class="valueHeader">Value</th>
                <th class="sellHeader">Buy</th>
                <th class="sellHeader">Reserve</th>
            </tr>
            % for hero in heroes:
                <tr id="${hero.id}Row">
                    <td class="heroImg" sorttable_customkey="${hero.name}"><img src="/static/images/dota/${hero.name.replace(" ", "_")}_icon.png" title="${hero.name}"/></td>
                    <td class="heroEntry">${hero.name}</td>
                    <td class="heroPointsEntry">${hero.points}</td>
                    <td class="picksEntry">${hero.picks}</td>
                    <td class="bansEntry">${hero.bans}</td>
                    <td class="winsEntry">${hero.wins}</td>
                    <td class="valueEntry">${hero.value}</td>
                    <td class="tradeEntry">
                        <form name="tradeForm" id="${hero.id}TradeForm" class="tradeForm" onsubmit="return false;">
                            <input type="hidden" value="${hero.id}" name="tradeHero"/>
                            <input type="hidden" value="0" name="tradeReserve"/>
                            <button type="submit" name="buyHero" class="btn waves-effect waves-light">Buy</button>
                        </form>
                    </td>
                    <td class="tradeEntry">
                        <form name="tradeForm" id="${hero.id}TradeForm" class="tradeForm" onsubmit="return false;">
                            <input type="hidden" value="${hero.id}" name="tradeHero"/>
                            <input type="hidden" value="1" name="tradeReserve"/>
                            <button type="submit" name="buyHero" class="btn waves-effect waves-light">Res</button>
                        </form>
                    </td>
                </tr>
            % endfor
        </table>
    </div>
</div>