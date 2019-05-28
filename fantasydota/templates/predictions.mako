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
    <span class="left">
    <h2>Predictions</h2>
    </span>
    <ul class="right">
            <li>
                <a class="dropdown-trigger btn leaderboardDropdown" data-hover="true" data-beloworigin="true" href="" data-activates="periodDropdown">
                Week
                <i class="material-icons right">arrow_drop_down</i></a>
            </li>
            <ul id="periodDropdown" class="dropdown-content">
            </ul>
        </ul>
        <span class="centre">
        <a id="leagueLink" target="_blank"></a></span>
</div>
<div class="row">
<div id="predictionsBlock" class="col m7 s12">
    <button type="submit" id="predictBtn" class="btn waves-effect waves-light">Update predictions</button>
    <div id="predictionsContainer">
    <table class="card-table striped centered" id="predictionsTable">
    </table>
    </div>
</div>

<script>
var period = ${period};

$( document ).ready(function() {
    $('.dropdown-trigger').dropdown();
    $(".dropdown-button").dropdown({
        "belowOrigin": true,
        "hover": true
    });
})
</script>
<script src="/static/predictions.js?v=1.0"></script>
