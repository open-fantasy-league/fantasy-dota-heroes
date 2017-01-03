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
    <p>
    Points are allocated in the following way:</br>
    <ul>
        <li>Pick/Ban  2 points</li>
        <li>Win       8 points</li>
        <li>Loss      -4 points</li>
    </ul></br>
        Bonus points:</br>
        <ul>
        <li>2nd Phase Pick/Ban/Win +1 point</li>
        <li>3rd Phase Pick/Ban/Win +2 point</li>
    </ul></br>

        (Picks and wins stack. so a 3rd phase pick will win earn 14 points total!)</br>

        Missing heroes penalty multiplier</br>
        <ul><li>x0.5 for every missing hero  (to prevent people abusing half-empty teams of best heroes)
        </li></ul>
    </p>

    <h2>Team</h2>
    <p>
    Your team can consist of up to 5 dota heroes (you are not required to use all 5, but will incur a penalty).
    </br>
    League team and Battlecup teams are separate. You will need to pick both.
    </br>
    Once tournament has started no transfers for league team are allowed throughout the tournament
    </br>
    Battlecup teams must be picked every-day (Hero values in battlecup mode will change throughout the tournament depending on their performance).
    </p>
</div>
