<%inherit file="layout.mako"/>

<%def name="title()">
    League Team
</%def>

<%def name="meta_keywords()">
    League, Dota, fantasy, points, game
</%def>

<%def name="meta_description()">
    League page for fantasy football cards game.
</%def>

<%def name="custom_css()">
</%def>

<div class="row" id="myTeamBlock">
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
    <div id="teamTableContainer" class="row">
        <table class="sortable card-table striped centered responsive-table" id="teamTable">
            <tr style="cursor: pointer" id="teamTableHeader">
                <th class="sellHeader">Remove</th>
                <th class="heroHeader">Player</th>
                <th class="positionHeader sorttable_numeric">Position</th>
                <th class="clubHeader sorttable_numeric">Club</th>
                <th class="pointsHeader sorttable_numeric">Points<br/>(Last week)</th>
                <th class="bonusHeader sorttable_numeric">Bonuses</th>
            </tr>
        </table>
    </div>
    <div class="row">
    <span class="left"><button type="submit" id="useWildcard" disabled="true" title="Wildcard sells entire team and resets to 50 credits" class="btn waves-effect waves-light" style="display:none">
        Use Wildcard</button></span>
    <span class="right"><button type="submit" id="confirmTransfers" disabled="true" class="btn waves-effect waves-light">Confirm Team!</button></span>
    </div>
</div>
<div id="heroesBlock" class="row">
    <h2><span class="col s12 m3">Cards (Credits: <strong><span class="userCredits"></span></strong>)</span><span class="col s12 m6 right">
    <button type="submit" id="newCardPack" title="5 credits" class="btn waves-effect waves-light amber accent-4">
    New pack<i class="material-icons right">shopping_cart</i>
    </button></h2>
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
    </div>
    <div id="cardsContainer" class="row">
        <ul class = "tabs">
        <li class = "tab col s3"><a href = "#goalkeepers">Goalkeepers</a></li>
        <li class = "tab col s3"><a href = "#defenders">Defenders</a></li>
        <li class = "tab col s3"><a href = "#midfielders">Midfielders</a></li>
        <li class = "tab col s3"><a href = "#forwards">Forwards</a></li>
        </ul>
        <div id="goalkeepers" class="col s12"></div>
        <div id="defenders" class="col s12"></div>
        <div id="midfielders" class="col s12"></div>
        <div id="forwards" class="col s12"></div>
    </div>
<script src="/static/trade.js?v=1.0"></script>
<script src="/static/team.js?v=1.1"></script>
