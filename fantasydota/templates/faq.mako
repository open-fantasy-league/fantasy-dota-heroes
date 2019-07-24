<%inherit file="fantasydota:templates/layout.mako"/>

<%def name="title()">
    FAQ
</%def>

<%def name="meta_keywords()">
    FAQ, frequently asked questions
</%def>

<%def name="meta_description()">
    FAQ page for fantasy dota
</%def>

<div>
<h2>What is this site?</h2>
    <div class="card-panel">
<p>
    Site for running open source fantasy leagues for various sports/esports. Current games are two styles of fantasy league for TI9, one picking pro players, one picking heroes.</p>
    </div>
<h2>Are there any prizes four tournament winner?</h2>
    <div class="card-panel">
<p>
   1st Prize Rubick arcana for pro league, 1st Prize Juggernaut arcana for hero league.
</p>
    </div>
<h2>Why do later phase picks/bans/wins get bonus points?</h2>
    <div class="card-panel">
<p>
This is so that people do not just instantly fill their team with the most imba-heroes who are guarantee 1st phase pick/ban<br>
A little bit of thought has to be put in to trade-off pick-rate with bonus points for less in demand heroes
</p>
    </div>
    <h2>Will you run this for other games?</h2>
    <div class="card-panel">
        <p>I have experimented with running similar one-off tournaments for Starcraft: Brood War and PUBG. Essentially any tournaments where I am watching all the games</p>
        <p>These one-off tournaments require a lot of effort from me (As opposed to the new DotA system which is fully automated). Therefore I will likely stick with Dota, and games with well developed API's</p>
    </div>
        <h2>Where do you get stats from?</h2>
    <div class="card-panel">
<p>
Combination of Valve official API and open-dota replay parsing of match.
</p>
    </div>
        <h2>Why is there a big points multiplier for main event?</h2>
    <div class="card-panel">
<p>
Because there are so many group games compared to main event, in the past, the tournament would be pretty much decided after the group stage.<br>
    If you weren't top ~15 after group stage...might as well give up.<br>
    With these multipliers you can still come back and win after a mediocre group stage performance.<br>

    There are less multipliers for the pro player league, as each player only plays a subset of the games, so their potential games doesn't drop as much
    as the heroes after the group stage.
</p>
    </div>
    <h2>Anything else...</h2>
    <div class="card-panel">
            <p>Send feedback/questions to fantasydotaeu@gmail.com or <a href="https://discord.gg/MAH7EEv" target=_blank">discord</a><br>
        Source-code available <a href="https://github.com/ThePianoDentist/open-fantasy-sports">here</a> (my instructions for setting up/running are abysmal, PM me for that)
            </p>
    </div>
</div>
