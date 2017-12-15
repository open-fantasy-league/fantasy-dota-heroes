<%inherit file="layout.mako"/>

<%def name="title()">
    Leaderboard: ${league.name}
</%def>

<%def name="meta_keywords()">
    Leaderboard, Dota, fantasy, points, game
</%def>

<%def name="meta_description()">
    Leaderboard page for fantasy dota game.
</%def>

<%def name="rank_by_fn(x, player, for_user)">
    % if x == "points":
        % if for_user:
            ${player.points_rank}
        % else:
            <% rounded_points = round(player.points, 1) %>
            ${int(rounded_points) if rounded_points.is_integer() else rounded_points}
        % endif
    % elif x == "wins":
        % if for_user:
            ${player.wins_rank}
        % else:
            ${player.wins}
        % endif
    % elif x == "picks":
        % if for_user:
            ${player.picks_rank}
        % else:
            ${player.picks}
        % endif
    % elif x == "bans":
        % if for_user:
            ${player.bans_rank}
        % else:
            ${player.bans}
        % endif
    % endif
</%def>

<%def name="getTime(period)">
${"period=%s" % period}
</%def>

<%def name="progress_arrow(i, player, x)">
    % if x == "points":
        <% old = player.old_points_rank %>
    % elif x == "wins":
        <% old = player.old_wins_rank %>
    % elif x == "picks":
        <% old = player.old_picks_rank %>
    % elif x == "bans":
        <% old = player.old_bans_rank %>
    % endif
    % if old:
        <% diff = i + 1 - old %>
        % if diff == 0:
            <span>&#8660;</span>
        % elif diff < -5:
            <span class="upMyArrow">&#8657;</span>
        % elif diff > 5:
            <span class="downMyArrow">&#8659;</span>
        % elif diff < 0:
            <span class="supMyArrow">&#8663;</span>
        % else:
            <span class="sdownMyArrow">&#8664;</span>
        % endif
    % endif
</%def>

<div class="row">
    <h2>${rank_by.title()} (${period.title() if period == "tournament" else "Day %d" % (int(period) + 1)})
        <a class="right" href="${league.url}" target="_blank">${league.name}</a></h2>
</div>
% if game.code == 'DOTA':
<div class="row">
<div id="leaderboardBlock" class="col s7">
    <nav>
    <div class="nav-wrapper teal darken-2">
        <ul class="left">
            <li class=${"active" if rank_by=="points" else ""}>
                <a id="pointsBtn" href="/leaderboard?rank_by=points&mode=${mode}&${getTime(period)}">
                    Points
                </a>
            </li>
            <li class=${"active" if rank_by=="wins" else ""}>
                <a id="winsBtn" href="/leaderboard?rank_by=wins&mode=${mode}&${getTime(period)}">
                    Wins
                </a>
            </li>
            <li class=${"active" if rank_by=="picks" else ""}>
                <a id="picksBtn" href="/leaderboard?rank_by=picks&mode=${mode}&${getTime(period)}">
                    Picks
                </a>
            </li>
            <li class=${"active" if rank_by=="bans" else ""}>
                <a id="bansBtn" href="/leaderboard?rank_by=bans&mode=${mode}&${getTime(period)}">
                    Bans
                </a>
            </li>
            <li>
                <a class="dropdown-button" data-hover="true" data-beloworigin="true" href="" data-activates="modeDropdown">${mode.title()}<i class="material-icons right">arrow_drop_down</i></a>
            </li>
            <ul id="modeDropdown" class="dropdown-content">
                <li><a href="/leaderboard?rank_by=${rank_by}&mode=${mode}">${mode.title()}</a></li>
                <li class="divider"></li>
                % for m in other_modes:
                    <li><a href="/leaderboard?rank_by=${rank_by}&mode=${m}">${m.title()}</a></li>
                % endfor
            </ul>
            <li>
                <a class="dropdown-button" data-hover="true" data-beloworigin="true" href="" data-activates="periodDropdown">Period<i class="material-icons right">arrow_drop_down</i></a>
            </li>
            <ul id="periodDropdown" class="dropdown-content">
                <li><a href="/leaderboard?rank_by=${rank_by}&mode=${mode}&period=tournament">Tournament</a></li>
                <li class="divider"></li>
                % for i in range(league.current_day + 1):
                    <li><a href="/daily?rank_by=${rank_by}&mode=${mode}&period=${i}">Day ${i+1}</a></li>
                % endfor
            </ul>
        </ul>
    </div>
    </nav>

    <div id="tableContainer">
        <table id="leaderboardTable" class="card-table striped centered">
            <tr>
                <th class="positionHeader">Position</th>
                <th class="playerHeader">Player</th>
                <th class="rankingHeader">${rank_by.title()}</th>
            </tr>
            % for i, player in enumerate(players):
                <tr class=${"playerRow" if not user or player.username != user.username else "userRow"}>
                    <td class="positionEntry">${i+1} ${progress_arrow(i, player, rank_by) if period == "tournament" and mode != "hero" else ""}
                    </td>
                    <td class="heroEntry">
                        <a href="${'/profile?user=%s' % player.user_id if mode != 'hero' else ''}"><span style="vertical-align:middle">
                        % if i == 0 and league.status == 2:
                          <img src="static/images/dota/trophy.png"/>
                            % endif
                            ${player.username}</span></a>
                    % if len(player_heroes) > i:
                        <span class="hero_images">
                        % for hero in player_heroes[i]:
                            <img src="/static/images/dota/${hero.replace(" ", "_")}_icon.png" title="${hero}"/>
                        % endfor
                        </span>
                    % endif
                    </td>
                    <td class="rankingEntry">${rank_by_fn(rank_by, player, False)}</td>
                </tr>
            % endfor
            % if user and mode == "global":
            <tr class="userRow outsideRanks">
                <td class="userRank">${rank_by_fn(rank_by, user, True)}</td>
                <td class="heroEntry">${user.username}</td>
                <td class="rankingEntry">${rank_by_fn(rank_by, user, False)}</td>
            </tr>
            % endif
        </table>
    </div>
</div>

    % elif game.code == 'PUBG':
    <div class="row">
<div id="leaderboardBlock" class="col s7">
    <nav>
    <div class="nav-wrapper teal darken-2">
        <ul class="left">
            <li class=${"active" if rank_by=="points" else ""}>
                <a id="pointsBtn" href="/leaderboard?rank_by=points&mode=${mode}&${getTime(period)}">
                    Points
                </a>
            </li>
            <li>
                <a class="dropdown-button" data-hover="true" data-beloworigin="true" href="" data-activates="modeDropdown">${mode.title()}<i class="material-icons right">arrow_drop_down</i></a>
            </li>
            <ul id="modeDropdown" class="dropdown-content">
                <li><a href="/leaderboard?rank_by=${rank_by}&mode=${mode}">${mode.title()}</a></li>
                <li class="divider"></li>
                % for m in other_modes:
                    <li><a href="/leaderboard?rank_by=${rank_by}&mode=${m}">${m.title()}</a></li>
                % endfor
            </ul>
            <li>
                <a class="dropdown-button" data-hover="true" data-beloworigin="true" href="" data-activates="periodDropdown">Period<i class="material-icons right">arrow_drop_down</i></a>
            </li>
            <ul id="periodDropdown" class="dropdown-content">
                <li><a href="/leaderboard?rank_by=${rank_by}&mode=${mode}&period=tournament">Tournament</a></li>
                <li class="divider"></li>
                % for i in range(league.current_day + 1):
                    <li><a href="/daily?rank_by=${rank_by}&mode=${mode}&period=${i}">Day ${i+1}</a></li>
                % endfor
            </ul>
        </ul>
    </div>
    </nav>

    <div id="tableContainer">
        <table id="leaderboardTable" class="card-table striped centered">
            <tr>
                <th class="positionHeader">Position</th>
                <th class="playerHeader">Player</th>
                <th class="rankingHeader">${rank_by.title()}</th>
            </tr>
            % for i, player in enumerate(players):
                <tr class=${"playerRow" if not user or player.username != user.username else "userRow"}>
                    <td class="positionEntry">${i+1} ${progress_arrow(i, player, rank_by) if period == "tournament" and mode != "hero" else ""}
                    </td>
                    <td class="heroEntry">

                        <span style="vertical-align:middle">
			% if player.username == "cav":
			<img src="/static/images/dota/trophy.png"/>
			% endif
                        ${player.username}</span>
                    % if len(player_heroes) > i:
                        <span class="hero_images">
                        % for hero in player_heroes[i]:
                            <img src="/static/images/pubg/teams/${hero.team.replace(" ", "_")}_icon.png" title="${hero.name}"/>
                        % endfor
                        </span>
                    % endif
                    </td>
                    <td class="rankingEntry">${rank_by_fn(rank_by, player, False)}</td>
                </tr>
            % endfor
            % if user and mode == "global":
            <tr class="userRow outsideRanks">
                <td class="userRank">${rank_by_fn(rank_by, user, True)}</td>
                <td class="heroEntry">${user.username}</td>
                <td class="rankingEntry">${rank_by_fn(rank_by, user, False)}</td>
            </tr>
            % endif
        </table>
    </div>
</div>
        %endif

<script>
$( document ).ready(function() {
    $(".dropdown-button").dropdown({
        "belowOrigin": true,
        "hover": true
    });
})
</script>
<div id="friendBlock" class="col s5">
    <div class="switch">
        <label>
          Off
          <input ${'checked=checked' if show_late_start else ''} type="checkbox" id="showLateStartCheckbox">
          <span class="lever"></span>
          Show late-starters
        </label>
    </div>
    % if game.code == "DOTA":
    <div class="card-panel">
    <p>2x points multiplier for day 2</p>
	<p>4x points multiplier for finals day</p>
        <p>Results updated ~2 minutes after match ends</p>
        <p><a href="https://discord.gg/MAH7EEv" target="_blank">Discord channel for suggestions/improvements</a></p>
        <p>Statistics provided by <a href="https://www.stratz.com" target="_blank">Stratz Esports <img src="/static/images/dota/stratz_icon.png"/></a></p>
    </div>
    % elif game.code == "PUBG":
        <div class="card-panel">
        <p>Thanks for playing everyone! COngratulations to overall winner cav! :D</p>
	<p> Due to IEM unexpectedly providing less detailed stats than they did in qualifiers, plus not scrolling end-game scoreboard. I can only accurately award kills points for top 12 squads. Apologies.</p>
        <p><a href="https://discord.gg/MAH7EEv" target="_blank">Discord channel for suggestions/improvements</a></p>
	                <p>This is independently run by me, no offiliation IEM</p><p>If there are bugs/problems it is my 100% fault and no reflection on IEM</p>
    </div>
    % endif
% if user:
    <div class="card">
    <div class="card-content">
        <p>
            Add friends usernames to compete in tables against them
        </p>
        <form name="addFriendForm" onsubmit="return false;">
            <input type="text" name="newFriend" placeholder="New friend..."/>
            <button type="submit" id="addFriendBtn" class="btn waves-effect waves-light">Add</button>
        </form>
    </div>
    </div>

    <script>
    $( document ).ready(function() {
        $(".dropdown-button").dropdown({"hover": true});
        function addFriendOnclick(){
            $.ajax({
                    url: "/addFriend",
                    type: "POST",
                    data: {"newFriend": $("input[name=newFriend]").val()},
                    success: function(data){
                        var success = data.success,
                        message = data.message;
                        if (!success){
                            sweetAlert(message);
                        }
                        else{
                            window.location.reload();
                        }
                    }
                }
            );
        };
        $("#addFriendBtn").click(addFriendOnclick);

        $('#showLateStartCheckbox').change( function() {
            var showLate = this.checked ? 1 : 0;
            var url = window.location.href;
            if (url.indexOf('showLate') > -1){
                url = url.replace(/(.*?)showLate=[01](.*?)/g, "$1showLate=" + showLate + "$2");
            }
            else if (url.indexOf('?') > -1){
               url += '&showLate=' + showLate
            }else{
               url += '?showLate=' + showLate
            }
            window.location.href = url;
        })
    })
    </script>
% endif
</div>
</div>
