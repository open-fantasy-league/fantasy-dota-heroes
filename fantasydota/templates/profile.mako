<%inherit file="layout.mako"/>

<%def name="title()">
   Profile
</%def>

<%def name="meta_keywords()">
    Profile, Dota, fantasy, points, game
</%def>

<%def name="meta_description()">
    Profile page for fantasy dota game.
</%def>

<div>
    <h5>Profile: ${username}</h5>
        <div class="row">
            <div class="card-panel">
                Highest Weekly Placing:
                Highest Daily Placing:
            </div>
        </div>
        <div class="row">
            % for achievement in achievements:
                <div class="col 2">
                    <div class="card-panel">
                        <span><strong>${achievement.name}</strong></span>
                        <span>${achievement.description}</span>
                        <img class="banIcon" src="/static/images/dota/${achievement.name.replace(' ', '_')}_icon.png" title="${achievement.name}"/>
                    </div>
                </div>
            % endfor
        </div>
    </div>
</div>