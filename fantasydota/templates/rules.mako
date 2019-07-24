<%inherit file="fantasydota:templates/layout.mako"/>

<%def name="title()">
     Rules / Scoring
</%def>

<%def name="meta_keywords()">
    Rules, fantasy, dota
</%def>

<%def name="meta_description()">
    Rules page for fantasy DotA cards
</%def>

<%def name="custom_css()">
</%def>

% if is_card_system:
    <div>
        <h2>Team</h2>
        <div class="card-panel">
        <p>Max of 2 players from each club.</p>
        <p>Teams are locked at start of game day, therefore any transfers you make, will only take affect start of next day
        (Old players will continue scoring 'this' day, even if removed from next day's team)</p>
        <p>
        You can earn credits for more card packs through <a href="/predictions">predicting correct series scores</a>.
        </p>
        </div>
        <h2>Scoring</h2>
        <div class="card-panel">
            Points are allocated in the following way:</br>
            <ul class="browser-default" id="scoringRules">
            </ul></br>
                <ul class="browser-default"><li>x2 points for final day
                </li>
                </ul>
                </br>
                Points leader at end of tournament wins Juggernaut arcana.
        </div>
    </div>

    <script src="/static/rules.js?v=1.0"></script>
% else:
<div>
    <h2>Team</h2>
    <div class="card-panel">
        <ul class="browser-default">
            <li>
                Your team must consist of 5 dota heroes
            </li>
            <li>
            You get 10 potential hero transfers to be used whenever you like throughout the tournament, as well as one wildcard, to reset your team and go back to 50 credits
            </li>
            <li>
            Transfers are processed at the start of each day, when teams are locked.
            </li>
            <li>
            Hero prices will fluctuate every day based on that days performance.
            </li>
        </ul>
    </div>
    <h2>Scoring</h2>
    <div class="card-panel">
        Points are allocated in the following way:</br>
        <ul class="browser-default">
            <li>Ban       1 points</li>
            <li>Pick      3 points</li>
            <li>Win       6 points</li>
            <li>Loss     -10 points</li>
        </ul></br>
            Bonus points:</br>
            <ul class="browser-default">
            <li>2nd Phase Pick/Ban/Win +1 point</li>
            <li>3rd Phase Pick/Ban/Win +3 point</li>
            </br>
                <li>(Picks and wins stack. A 3rd phase pick and win will earn 15 points total!)</li>
                            </br>
                <li>(Win/Loss applies to picked heroes, but not banned heroes.)</li>
        </ul>
            Only full teams of 5 heroes will score points</br>
         Example:</br>
        <img src="/static/images/dota/examplescoring.png"></img></br>
            Main event multiplier:</br>
            <ul class="browser-default"><li>x2 points for Main event matches. x3 points for grand finals day!
            </li>
            </ul>
            </br>
            Points leader at end of tournament wins Rubick arcana.
    </div>
</div>
% endif