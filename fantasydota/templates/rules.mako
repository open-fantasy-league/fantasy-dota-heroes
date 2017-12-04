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

% if game_code == 'DOTA':
<div>
    <h2>Scoring</h2>
    <div class="card-panel">
        Points are allocated in the following way:</br>
        <ul class="browser-default">
            <li>Ban       1 points</li>
            <li>Pick      2 points</li>
            <li>Win       6 points</li>
            <li>Loss     -8 points</li>
        </ul></br>
            Bonus points:</br>
            <ul class="browser-default">
            <li>2nd Phase Pick/Ban/Win +1 point</li>
            <li>3rd Phase Pick/Ban/Win +3 point</li>
            </br>
                <li>(Picks and wins stack. A 3rd phase pick will win earn 14 points total!)</li>
                            </br>
                <li>(Win/Loss applies to picked heroes, but not banned heroes.)</li>
        </ul>
            Missing heroes penalty multiplier:</br>
            <ul class="browser-default"><li>x0.5 for every missing hero  (to prevent people abusing half-empty teams of best heroes)
            </li></ul>
            Main event multiplier:</br>
            <ul class="browser-default"><li>x2 points for second day matches
            </li>
            </ul>
            <ul class="browser-default"><li>x4 points for final day matches
            </li>
            </ul>
    </div>
    <h2>Team</h2>
    <div class="card-panel">
        <ul class="browser-default">
            <li>
                Your Main team can consist of up to 5 dota heroes (you are not required to use all 5, but you incur a heavy percentage penalty for each missing hero).
            </li>
            <li>
                Your Reserve team also consists of up to 4 heroes, worth 40 credits. These earn 0 points whilst in your reserves. But they can be swapped into your main team midway through the tournament.
            </li>
            <li>
            Your main team will always have a 50 credit limit. i.e. You must remove 20 credits worth of heroes from Main team, before promoting a reserve hero worth 20 credits.
            </li>
            <li>
            Hero values will remain static throughout the tournament.
            </li>
        </ul>
    </div>
</div>
%elif game_code == 'PUBG':
<div>
    <h2>Scoring</h2>
    <div class="card-panel">
        Points are allocated in the following way:</br>
        <ul class="browser-default">
            <li>Kill&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2 points</li>
            <li>Win&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;5 points</li>
            <li>Top 3&nbsp;&nbsp;&nbsp;&nbsp; 3 points</li>
            <li>Top 5&nbsp;&nbsp;&nbsp;&nbsp; 2 points</li>
            <li>Top 10&nbsp;&nbsp;&nbsp;1 point</li>
        </ul></br>
            Missing players penalty multiplier:</br>
            <ul class="browser-default"><li>x0.5 for every missing player
            </li></ul>
    </br>
        Points are weighted heavily towards kills over position because that seems fun to me.
    </br>
        Points system has to be simple until PUBG has available data API's or replay systems.
    </div>
    <h2>Team</h2>
    <div class="card-panel">
        <ul class="browser-default">
            <li>
                Your Main team can consist of up to 4 players (You can pick under 4, but will incur a 50% points penalty for each missing player. Hint: Just pick 4!)
            </li>
            <li>
                Your Reserve team also consists of up to 2 players. These earn 0 points whilst in your reserves. But they can be swapped into your main team between tournament days.
            </li>
            <li>
                You are only allowed one player from each PUBG team in your main team. You can have a second TSM, Liquid etc player in your reserves, however you can only swap him in for the other TSM, Liquid player in main team.
            </li>
            <li>
            The credit values do not really mean anything right now. However for future tournaments, players may be assigned different values based on their perceived ability.
            </li>
        </ul>
    </div>
</div>

%endif
