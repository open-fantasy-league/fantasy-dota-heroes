<%inherit file="layout.mako"/>

<%def name="custom_css()">
    <link href="/static/footballteams.css?v=1.0" rel="stylesheet"/>
</%def>

<%def name="title()">
    Card collection
</%def>

<%def name="meta_keywords()">

</%def>

<%def name="meta_description()">
    Card collection for fantasy DotA
</%def>

<div class="row">
    <h2>Commissioner</h2>
    <div id="cardsContainer" class="row">
    <ul>
        % for league in commissioned_leagues:
            <a data-id="${league.id}" class="leagueLink">${league.name}</a>
        % endfor
        % for league in commissioned_leagues:
            <div id="leagueContainer${league.id}" class="leagueSection row hide" >
                <form method="POST" id="leagueForm${league.id}" data-id="${league.id}" class="updateForm">
                    <input type="hidden" name="league_id" value="${league.id}">
                    <div class="input-field row">
                        Name:<input type="text" name="name">
                    </div>
                    <div class="input-field row">
                        Invite link:<input type="text" name="invite" value="${league.full_invite_link}" disabled>
                    </div>
                    <div class="input-field row">
                        Draft start (format '2019-12-27 22:44:30' Time UTC)<input type="text" name="start">
                    </div>
                    <div class="input-field row">
                        Draft next deadline<input type="text" name="nextDeadline">
                    </div>
                    <div class="input-field row">
                        Draft timer (Seconds between each pick)<input type="text" name="timer">
                    </div>
                    <div class="row switch">
                        Manual draft<i class="material-icons"
                        title="Draft yourself, i.e. in discord, and submit resulting draft later">help</i>:
                        <label>
                            Off
                            <input type="checkbox" class="manualDraftBtn" name="manualDraftBtn" autocomplete="off">
                            <span class="lever"></span>
                            On
                        </label>
                    </div>
                    <div class="input-field row">
                        Override draft order <i class="material-icons"
                        title="To override randomly selected draft order, or reset it if something goes wrong. Comma separated list of team names">help</i>
                        :<input type="text" name="order">
                    </div>
                    <div class="row">
                        <button class="btn waves-effect waves-light" type="submit" name="action">Submit
                        <i class="material-icons right">send</i>
                        </button>
                    </div>
                </form>
                <div class="row">
                     <button class="btn waves-effect waves-light generateDraftOrderBtn" type="button" data-id="${league.id}">
                        Generate Draft Order
                        <i class="material-icons right"
                        title="When all friends/players have joined your league, this makes a randomised draft order from them">help</i>
                    </button>
                </div>
                <div class="row switch">
                    Pause Draft:
                    <label>
                        Unpaused
                        <input type="checkbox" class="pauseDraftBtn" name="pauseDraftBtn" autocomplete="off" onchange="togglePaused(this);" data-id="${league.id}">
                        <span class="lever"></span>
                        Paused
                    </label>
                </div>
            </div>
        % endfor
    </ul>
    <a data-id="0" class="leagueLink">New League</a>
        <div id="leagueContainer0" class="leagueSection row hide">
            <form method="POST" id="leagueFormNew" data-id="0">
                    <div class="input-field row">
                        Name:<input type="text" name="name">
                    </div>
                    <div class="input-field row">
                        Draft start (format '2019-12-27 22:44:30' Time UTC)<input type="text" name="start" placerholder="2019-12-27 22:44:30">
                    </div>
                    <div class="input-field row">
                        Draft timer (Seconds between each pick)<input type="text" name="timer" placeholder="120">
                    </div>
                    <div class="row switch">
                        Manual draft<i class="material-icons"
                        title="Draft yourself, i.e. in discord, and submit resulting draft later">help</i>:
                        <label>
                            Off
                            <input type="checkbox" class="manualDraftBtn" name="manualDraftBtn" autocomplete="off">
                            <span class="lever"></span>
                            On
                        </label>
                    </div>
                    <div class="input-field row">
                        <button class="btn waves-effect waves-light" type="submit" name="action">Submit
                        <i class="material-icons right">send</i>
                        </button>
                    </div>
            </form>
        </div>
    </div>
</div>
<script>var apiKey = "${api_key}" // This is just your personal api-key, and it isn't shown to other users</script>
<script src="/static/commissioner.js?v=1.0"></script>