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
    <h5>Profile: ${shown_user.username}</h5>
        <div class="row">
            <div class="card-panel">
                Level: ${user_xp.level or '-'}
                Xp: ${user_xp.xp}
                Highest Weekly Placing: ${user_xp.highest_weekly_pos or '-'}
                Highest Daily Placing: ${user_xp.highest_daily_pos or '-'}
                All time points
            </div>
        </div>
        <div class="row">
            % for achievement in achievements:
                <div class="col 2">
                    <div class="card-panel">
                        <span><strong>${achievement.name}</strong></span>
                        <span>${achievement.description}</span>
                        <img class="banIcon" src="/static/images/dota/achievements/${achievement.id}.png" title="${achievement.name}"/>
                    </div>
                </div>
            % endfor
        </div>
    </div>
</div>