<%inherit file="fantasydota:templates/layout.mako"/>

<%def name="title()">
    Fantasy Football Cards
</%def>

<%def name="meta_keywords()">
    Fantasy Football Cards, Home
</%def>

<%def name="meta_description()">
    Home page for Fantasy Football Cards
</%def>

<%def name="custom_css()">
</%def>

<div class="row">
    <div class="card-panel">
        <h1>A free-to-play, open-source, fantasy football league; styled on ultimate team, with card packs and stat bonuses (minus the pay-2-win)</h1>
        <h3>1. <a href="/login">Login</a> with steam, google, or site account</h3>
        <h3>2. Click <a href="/team">Team</a></h3>
        <h3>3. Buy some card packs (5 credits each. 50 starting credits). Gold and silver cards have stat multipliers for greater points hauls</h3>
        <img src="/static/images/cardpackexample.png" />
        <h3>4. Make a 4-4-2 team from your best cards</h3>
        <img src="/static/images/teamexample.png" />
        <h3>5. Earn (or lose) points based on goals, assists, conceded, cards, missed penalties,
         high <a href="https://www.fotmob.com">Fotmob</a> match ratings</h3>
        <h3>6. Go to <a href="/predictions">Predictions</a> to earn credits for more/better cards by predicting correct match scores</h3>
        <img src="/static/images/predictionsexample.png" />
    </div>
</div>