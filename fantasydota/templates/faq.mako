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
    Simple fantasy dota style game but with heroes. You buy the heroes you think are likely to be picked/banned and win in pro matches.<br>
When this occurs you gain points.</p>
        <p>
            Each league lasts a week. You can pre-purchase your team for the following week to receive full XP.</p>
    </div>
        <h2>What games score points?</h2>
    <div class="card-panel">
        <p>Every single Pro Circuit tournament, Major and Minor, is recorded and scored. This includes qualifiers (except open qualifiers)
        </p>
    </div>
<h2>Are there any prizes?</h2>
    <div class="card-panel">
<p>
    No physical prizes [May be added in later], however there is an reward system. You earn XP from completing achievements, as well as based upon final standings at the end of each week.
</p>
    </div>
    <h2>What time does League/Day rollover?</h2>
    <div class="card-panel">
<p>League/Day's roll over at 6AM GMT, 1AM EST, 10PM PST. Any games that start before the deadline, yet end after it are counted in the new week, not the old week.
</p>
    </div>
<h2>Aren't there already fantasy dota games?</h2>
    <div class="card-panel">
<p>
Yeah there's the official stuff, and other third party stuff.<br>
My problem with these is being based on pro players, I have to keep track of what teams are playing on what days,
who's been knocked out, which Chinese Dota players are good etc.<br>
I find this system to be a lot easier to get into.
</p>
    </div>
<h2>Why do later phase picks/bans/wins get bonus points?</h2>
    <div class="card-panel">
<p>
This is so that people do not just instantly fill their team with the most imba-heroes who are guarantee 1st phase pick/ban<br>
A little bit of thought has to be put in to trade-off pick-rate with bonus points for less in demand heroes
</p>
    </div>
    <h2>A match from a pro circuit tournament is missing!</h2>
    <div class="card-panel">
        <p>In some rare cases, such as a game/lobby crash. A captain's mode game will be re-made as an all-pick game.</p>
        <p>Therefore the picks/bans for this game cannot be found in the Dota 2 API</p>
        <p>My official stance on these missing games is I will attempt to retroactively input the match and update points</p>
        <p>However if I am on holiday or too busy, I cannot guarantee I will be able to manually update</p>
    </div>
    <h2>Will you run this for other games?</h2>
    <div class="card-panel">
        <p>I have experimented with running similar one-off tournaments for Starcraft: Brood War and PUBG. Essentially any tournaments where I am watching all the games</p>
        <p>These one-off tournaments require a lot of effort from me (As opposed to the new DotA system which is fully automated). Therefore I will likely stick with Dota, and games with well developed API's</p>
    </div>
    <h2>I want to run a fantasy league like this for my tournament</h2>
        <div class="card-panel">
        <p>I can add a league which is separate from weekly leagues and only scores points on your tournament</p>
            <p>So long as you provide any prizes I'm happy to do this for free.</p>
            <p>If you want to hold it on your site or through a twitch/reddit interface I'm happy to help/advise where possible</p>
    </div>
    <h2>Anything else...</h2>
    <div class="card-panel">
            <p>Send feedback/questions to fantasydotaeu@gmail.com or <a href="https://discord.gg/MAH7EEv" target=_blank">discord</a><br>
        Source-code available <a href="https://github.com/ThePianoDentist/fantasy-dota-heroes">here</a> (my instructions for setting up/running are abysmal, PM me for that)
            </p>
    </div>
    <h2>Thanks/Shout-outs</h2>
    <div class="card-panel">
        <p>
        Whilst the code is all my own work, I would like to thank everyone who plays. Without any players, there's not much point in the site!
        Special thanks to Noxville [Idea for having 'reserves' that can be swapped into main team, which adds a really well balanced bit of strategy] and Kriger, who is active in discord channel and will often feedback on ideas/suggestions I propose.
        </p>
    </div>
    <!--<h2>Why is there a big points multiplier for main event?</h2>-->
    <!--<div class="card-panel">-->
<!--<p>-->
<!--Because there are so many group games compared to main event, in the past, the tournament would be pretty much decided after the group stage.<br>-->
    <!--If you weren't top ~15 after group stage...might as well give up.<br>-->
    <!--With these multipliers you can still come back and win after a mediocre group stage performance.-->
<!--</p>-->
    <!--</div>-->
</div>
