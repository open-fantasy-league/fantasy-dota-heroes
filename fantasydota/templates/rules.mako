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
        <li>Ban       1 points</li>
        <li>Pick      2 points</li>
        <li>Win       6 points</li>
        <li>Loss     -5 points</li>
    </ul></br>
        Bonus points:</br>
        <ul>
        <li>2nd Phase Pick/Ban/Win +1 point</li>
        <li>3rd Phase Pick/Ban/Win +3 point</li>
    </ul></br>

        (Picks and wins stack. so a 3rd phase pick will win earn 14 points total!)</br>

        Missing heroes penalty multiplier</br>
        <ul><li>x0.5 for every missing hero  (to prevent people abusing half-empty teams of best heroes)
        </li></ul>
    </p>

    <h2>Team</h2>
    <p>
    Your team can consist of up to 5 dota heroes (you are not required to use all 5, but you incur percentage penalty for each missing hero).
    </br>
    Unlimited transfers can take place every day, between games
    </br>
        Hero values will be slightly reclibrated every day
    </br>
        Selling a hero simply refunds the cost you paid for it, not it's current value
    </br>
    </p>
</div>
