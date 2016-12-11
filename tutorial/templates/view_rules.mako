<%inherit file="tutorial:templates/layout.mako"/>

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
    There are unlimited transfers, however transfer window will close each day, whilst games are taking place.
    </br>
    Transfer window closes ~30minutes before 1st game of the day, opens after the last one.</br>
Transfers can still take place during window closure, however no points are earned on new heroes until next day.
    </p>
</div>
