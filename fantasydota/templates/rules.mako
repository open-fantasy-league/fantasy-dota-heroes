<%inherit file="fantasydota:templates/layout.mako"/>

<%def name="title()">
     Rules / Scoring
</%def>

<%def name="meta_keywords()">
    Rules, fantasy, dota
</%def>

<%def name="meta_description()">
    Rules page for fantasy dota
</%def>

<div>
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
            Weekend multiplier:</br>
            <ul class="browser-default"><li>x2 points for Main event matches. x3 points for grand finals day!
            </li>
            </ul>
            </br>
            Points leader at end of tournament wins Rubick arcana.
    </div>
    <h2>Team</h2>
    <div class="card-panel">
        <ul class="browser-default">
            <li>
                Your team must consist of 5 dota heroes
            </li>
            <li>
            You get 5 potential hero transfers to be used whenever you like throughout the tournament, as well as one wildcard, to reset your team and go back to 50 credits
            There is a 1 hour delay before your mid-tournament transfers go through. This prevents abuse of transferring as drafts/games occurring.
            </li>
        </ul>
    </div>
</div>
