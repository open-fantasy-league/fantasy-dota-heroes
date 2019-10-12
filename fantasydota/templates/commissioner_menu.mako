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
            <div id="leagueContainer${league.id}" class="leagueSection row hide" >
                <form method="POST" id="leagueForm${league.id}" data-id="${league.id}" class="updateForm">
                    <input type="hidden" name="league_id" value="${league.id}">
                    <div class="input-field col s4">
                        Name:<input type="text" name="name">
                    </div>
                    <div class="input-field col s4">
                        Invite link:<input type="text" name="invite" value="${league.full_invite_link}" disabled>
                    </div>
                    <div class="input-field col s4">
                        Draft start (format '2019-12-27 22:44:30' Time UTC)<input type="text" name="start">
                    </div>
                    <div class="input-field col s4">
                        Draft next deadline<input type="text" name="nextDeadline">
                    </div>
                    <div class="input-field col s4">
                        Draft timer (Seconds between each pick)<input type="text" name="timer">
                    </div>
                    <div class="input-field col s4">
                        Manual draft(Draft yourself, i.e. in discord, and submit resulting draft later):<input type="text" name="manual" alt="Rather than draft through this site. You carry out draft yourself, i.e. Discord, and simply record results here">
                    </div>
                    <div class="input-field col s4">
                        Draft order (to override randomly selected draft order):<input type="text" name="order" alt="Comma separated list of usernames">
                    </div>
                    <div class="input-field col s4">
                        <button class="btn waves-effect waves-light" type="submit" name="action">Submit
                        <i class="material-icons right">send</i>
                        </button>
                    </div>
                </form>
            </div>
        % endfor
    </ul>
    <a data-id="0" class="leagueLink">New League</a>
        <div id="leagueContainer0" class="leagueSection row hide">
            <form method="POST" id="leagueFormNew" data-id="0">
                    <div class="input-field col s4">
                        Name:<input type="text" name="name">
                    </div>
                    <div class="input-field col s4">
                        Draft start (format '2019-12-27 22:44:30' Time UTC)<input type="text" name="start" placerholder="2019-12-27 22:44:30">
                    </div>
                    <div class="input-field col s4">
                        Draft timer (Seconds between each pick)<input type="text" name="timer" placeholder="120">
                    </div>
                    <div class="input-field col s4">
                        Manual draft(Draft yourself, i.e. in discord, and submit resulting draft later):<input type="text" name="manual" alt="Rather than draft through this site. You carry out draft yourself, i.e. Discord, and simply record results here">
                    </div>
                    <div class="input-field col s4">
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