<%inherit file="layout.mako"/>

<%def name="title()">
    League Team
</%def>

<%def name="meta_keywords()">
    League, Dota, fantasy, points, game
</%def>

<%def name="meta_description()">
    League page for fantasy DotA cards game.
</%def>

<%def name="custom_css()">
</%def>

<div class="row" id="myTeamBlock">
    <div class="switch" id="activeTeamSwitchDiv">
    <label>
      Future
      <input type="checkbox" id="activeTeamBtn" onchange="switchActiveTeam(this);" autocomplete="off">
      <span class="lever"></span>
      Active
    </label>
    </div>
    <div class="row">
    <span class="left" style="width: 33%;"><h5><span class="col s3 hide-on-small-only">Team: </span>
        <button id="updateNameButton"><i class="material-icons prefix">edit</i></button>
    <button id="confirmNameButton" class="hide"><i class="material-icons prefix">check</i></button>
    <span id="teamName">${team_name if user else ""}</span>
    <span id="teamNameEdit" class="hide">
          <input id="teamNameTextField" type="text" class="validate" value=${team_name if user else ""} />
        </span>
    </h5></span>
    <span class="left center-align hide-on-small-only" style="width: 33%;"><h5><a id="leagueLink" target="_blank"></a></h5></span>
    <span class="right"><h5>Points: <span class="userPoints"></span></h5></span>
    </div>
    % if is_card_system:
    <div id="teamTableContainer" class="row">
        <table class="sortable card-table striped centered responsive-table" id="teamTable">
            <tr style="cursor: pointer" id="teamTableHeader">
                <th class="sellHeader">Remove</th>
                <th class="heroHeader">Player</th>
                <th class="positionHeader sorttable_numeric">Position</th>
                <th class="clubHeader sorttable_numeric">Team</th>
                <th class="pointsHeader sorttable_numeric">Points<br/>(Last day)</th>
                <th class="bonusHeader sorttable_numeric">Bonuses</th>
            </tr>
        </table>
    </div>
    % else:
        <div id="teamTableContainer">
        <table class="sortable card-table striped centered" id="teamTable">
            <tr style="cursor: pointer" id="teamTableHeader">
                <th class="sellHeader">Sell</th>
                <th class="heroHeader">Hero</th>
                <th class="dummyHeader" colspan="0"></th>
                <th class="heroPointsHeader sorttable_numeric">Points</th>
                <th class="picksHeader extra sorttable_numeric">Picks</th>
                <th class="bansHeader extra sorttable_numeric">Bans</th>
                <th class="winsHeader extra sorttable_numeric">Wins</th>
                <th class="valueHeader sorttable_numeric">Value</th>
            </tr>
        </table>
    </div>
    % endif
</div>
<div id="heroesBlock" class="row">
<div class="card-panel">
    <div class="card-content">
        %if is_card_system:
            <p><button type="submit" id="newCardPack" title="5 credits" class="btn waves-effect waves-light amber accent-4 grey-text text-darken-3">
    New pack<i class="material-icons right">shopping_cart</i>
    </button> <span class="center">50 Credits to buy cards and form a team of 5 players (max 2 from each team)</span>
    <span class="right"><button type="submit" id="confirmTransfers" disabled="true" class="btn waves-effect waves-light orange darken-3 floatBottomLeft">Confirm Team!</button></span>
    </p>
        % else:
            <div class="row"><span class="col m4 s12 right"><button type="submit" id="useWildcard" disabled="true" title="Wildcard sells entire team and resets to 50 credits" class="btn waves-effect waves-light hide">
        Use Wildcard</button></span><span class="col m4 s12">50 Credits to pick a team of 5 heroes</span>
        <span class="col m4 s12"><button type="submit" id="confirmTransfers" disabled="true" class="btn waves-effect waves-light orange darken-3 floatBottomLeft">Confirm Team!</button></span>
        </div>
        %endif
        <div class="row"><span id="transferDelayMessage" class="hide left">
            Transfers processed at start of next game day.</span>
        <span id="remainingTransfersSection" class="hide right"><span id="remainingTransfers"></span> remaining transfers available
        </span>
        <span id="infinityTransfersUntilStartMessage" class="hide left">Infinite transfers before tournament starts. 10 available transfers during tournament.</span>
        </div>
    </div>
    </div>
% if is_card_system:
    <h2><span class="col s12 m6">Cards (Credits: <strong><span class="userCredits"></span></strong>)</span><span class="col s12 m6 right"></h2>
</div>
    <div id="cardFilters" class="row">
        <div class="col s1"><button type="button" id="filterCards" class="btn waves-effect waves-light">Filter</button></div>
        <div class="col s3">
            <label for="cardTeamFilter"><h6>Team:</h6></label>
            <input id="cardTeamFilter" type="text" class="validate" value="" />
        </div>
        <div class="col s3">
            <label for="cardPlayerFilter"><h6>Player:</h6></label>
            <input id="cardPlayerFilter" type="text" class="validate" value="" />
        </div>
        <div class="col s5">
            <input id="goldFilter" type="checkbox" class="filled-in" checked="checked" />
            <label for="goldFilter">Gold</label>
            <input id="silverFilter" type="checkbox" class="filled-in" checked="checked" />
            <label for="silverFilter">Silver</label>
            <input id="bronzeFilter" type="checkbox" class="filled-in" checked="checked" />
            <label for="bronzeFilter">Bronze</label>
        </div>
            <span><button type="submit" id="recycleFiltered" title="Recycle all cards under currently selected filters" class="btn waves-effect waves-light">
        Recycle filtered</button></span>
        <span><button type="submit" id="recycleDupeCommons" title="Recycle all commons that are duplicates of same player" class="btn waves-effect waves-light">
        Recycle common duplicates</button></span>
    </div>
    <div id="cardsContainer" class="row">
        <ul class = "tabs">
        <li class = "tab col s4"><a href = "#supports">Support</a></li>
        <li class = "tab col s4"><a href = "#cores">Core</a></li>
        <li class = "tab col s4"><a href = "#offlanes">Offlane</a></li>
        </ul>
        <div id="supports" class="col s12"></div>
        <div id="cores" class="col s12"></div>
        <div id="offlanes" class="col s12"></div>
    </div>
    <script src="/static/trade.js?v=1.2"></script>
<script src="/static/team.js?v=1.2"></script>
%else:
    <h2>Heroes (Credits Available: <strong><span class="userCredits"></span></strong>)</h2>
      <div class="switch">
    <label>
      Table view (sortable)
      <input type="checkbox" id="gridViewBtn" onchange="switchGridTable(this);" checked autocomplete="off">
      <span class="lever"></span>
      Grid view
    </label>
  </div>
    <div id="gridContainer">
        <table class="card-table striped centered" id="heroesTableGrid">
        <tr><td></td></tr>
        </table>
    </div>
    <div id="tableContainer" style="display:none">
        <table class="sortable card-table striped centered" id="heroesTable">
            <tr style="cursor: pointer" id="heroesTableHeader">
                <th class="sellHeader">Buy</th>
                <th class="heroHeader">Hero</th>
                <th class="dummyHeader" colspan="0"></th>
                <th class="heroPointsHeader sorttable_numeric">Points</th>
                <th class="picksHeader extra sorttable_numeric">Picks</th>
                <th class="bansHeader extra sorttable_numeric">Bans</th>
                <th class="winsHeader extra sorttable_numeric">Wins</th>
                <th class="valueHeader sorttable_numeric">Value</th>
            </tr>
        </table>
    </div>
    </div>
    <script src="/static/hero_trade.js?v=1.0"></script>
<script src="/static/hero_team.js?v=1.1"></script>
%endif
<script src="/static/teamname.js?v=1.0"></script>
