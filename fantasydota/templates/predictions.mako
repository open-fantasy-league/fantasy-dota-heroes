<%inherit file="layout.mako"/>

<%def name="title()">
    Leaderboard
</%def>

<%def name="meta_keywords()">
    Leaderboard, Dota, fantasy, points, game
</%def>

<%def name="meta_description()">
    Leaderboard page for fantasy dota game.
</%def>

<div class="row">
    <h2>Predictions
        <a class="right" id="leagueLink" target="_blank"></a></h2>
</div>
<div class="row">
<div id="predictionsBlock" class="col m7 s12">
    <nav>
    <div class="nav-wrapper teal darken-2">
        <ul class="left">
            <li>
                <a class="dropdown-button leaderboardDropdown" data-hover="true" data-beloworigin="true" href="" data-activates="periodDropdown">Period<i class="material-icons right">arrow_drop_down</i></a>
            </li>
            <ul id="periodDropdown" class="dropdown-content">
            </ul>
        </ul>
    </div>
    </nav>

    <div id="predictionsContainer">
    </div>
</div>

<script>
var period = ${period};

$( document ).ready(function() {
    $(".dropdown-button").dropdown({
        "belowOrigin": true,
        "hover": true
    });
})
</script>
<script src="/static/predictions.js?v=1.0"></script>
