<%inherit file="layout.mako"/>

<%def name="title()">
    League Team
</%def>

<%def name="meta_keywords()">
    League, Dota, fantasy, points, game
</%def>

<%def name="meta_description()">
    League page for fantasy dota game.
</%def>

<div class="row" id="myTeamBlock">
    <span class="left"><h2>Team</h2></span>
    <span class="right"><h2>Points: <span class="userPoints"></span></h2></span>
    <div id="tableContainer">
        <table class="sortable card-table striped centered" id="teamTable">
            <tr style="cursor: pointer" id="teamTableHeader">
                <th class="heroHeader">Hero</th>
                <th class="dummyHeader" colspan="0"></th>
                <th class="heroPointsHeader sorttable_numeric">Points</th>
                <th class="picksHeader extra sorttable_numeric">Picks</th>
                <th class="bansHeader extra sorttable_numeric">Bans</th>
                <th class="winsHeader extra sorttable_numeric">Wins</th>
                <th class="valueHeader sorttable_numeric">Value</th>
                <th class="sellHeader">Sell</th>
            </tr>
        </table>
    </div>
    <span class="left"><button type="submit" id="useWildcard" disabled="true" title="Wildcard sells entire team and resets to 50 credits" class="btn waves-effect waves-light" style="display:none">
        Use Wildcard</button></span>
    <span class="right"><button type="submit" id="confirmTransfers" disabled="true" class="btn waves-effect waves-light">Confirm Team!</button></span>
</div>

<div class="card row">
    <div class="card-content">
        <p><span id="pleaseLogIn" style="display:none" class="messageTransClosed"><strong>Please log in or register to pick a team</strong></span></p>
        <p>50 Credits to pick a team of 5 heroes</p>
        <span id="remainingTransfersSection" style="display:none">You have <span id="remainingTransfers"></span> remaining available transfers (Transfers will not count until 'Confirm Transfers' pressed)
        </span>
        <span id="wildcardDescriptionMessage" style="display:none">Wildcard sells entire team and resets to 50 credits</span>
        <span id="transferDelayMessage"><p><strong>
            There is a 1 hour delay between confirmation of transfers and their processing (to prevent cheating/unfair advantages).
        </strong></p>
        <p>Further transfers are disabled during this hour period,
        however your old team does continue scoring points until transfers processed</p></span>
        <span class="messageTransClosed" id="messageTransferCooldown" style="display:none"><p><strong>
            Due to recent changes you are in transfer cooldown.
        </strong></p></span>
        <span id="infinityTransfersUntilStartMessage" style="display:none">Once the tournament starts you will have 5 extra transfers you can make (You can make infinity changes before first game)</span>
        <p><strong><a href="/rules">Detailed Rules</a></strong></p>
        <span>
            <p>Tables are sortable (click table headers)</p>
        </span>
    </div>
</div>
<div id="heroesBlock" class="row">
    <h2>Heroes (Credits Available: <span class="userCredits"></span>)</h2>
    <div id="tableContainer">
        <table class="sortable card-table striped centered" id="heroesTable">
            <tr style="cursor: pointer" id="heroesTableHeader">
                <th class="heroHeader">Hero</th>
                <th class="dummyHeader" colspan="0"></th>
                <th class="heroPointsHeader sorttable_numeric">Points</th>
                <th class="picksHeader extra sorttable_numeric">Picks</th>
                <th class="bansHeader extra sorttable_numeric">Bans</th>
                <th class="winsHeader extra sorttable_numeric">Wins</th>
                <th class="valueHeader sorttable_numeric">Value</th>
                <th class="sellHeader">Buy</th>
            </tr>
        </table>
    </div>
</div>
<script src="/static/trade.js"></script>
<script src="/static/team.js"></script>
