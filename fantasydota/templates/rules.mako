<%inherit file="fantasydota:templates/layout.mako"/>

<%def name="title()">
     Rules / Scoring
</%def>

<%def name="meta_keywords()">
    Rules, fantasy, dota
</%def>

<%def name="meta_description()">
    Rules page for fantasy football cards
</%def>

<%def name="custom_css()">
</%def>

<div>
    <h2>Team</h2>
    <div class="card-panel">
    <p>Max of 2 players from each club.</p>
    <p>Teams are locked at start of game week, therefore any transfers you make, will only take affect start of next week
    (Old players will continue scoring 'this' week, even if removed from next week's team)</p>
    </div>
    <h2>Scoring</h2>
    <div class="card-panel">
        Points are allocated in the following way:</br>
        <ul class="browser-default" id="scoringRules">
        </ul></br>
            <ul class="browser-default"><li>x2 points for final week
            </li>
            </ul>
            </br>
            Prizes TBD closer to start
    </div>
</div>

<script src="/static/rules.js?v=1.0"></script>
