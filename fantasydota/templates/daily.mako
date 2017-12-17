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
<div id="leaderboardBlock" class="col s12 m6">
    <nav>
    <div class="nav-wrapper teal darken-2">
        <ul class="left">
            <li>
                <a class="dropdown-button" data-hover="true" data-beloworigin="true" href="" data-activates="rankbyDropdown">${rank_by.title()}<i class="material-icons right">arrow_drop_down</i></a>
            </li>
            <ul id="rankbyDropdown" class="dropdown-content">
                % if rank_by != "points":
                    <li><a href="/leaderboard?rank_by=points&mode=${mode}">Points</a></li>
                % endif
                % if rank_by != "wins":
                    <li><a href="/leaderboard?rank_by=wins&mode=${mode}">Wins</a></li>
                % endif
                % if rank_by != "picks":
                    <li><a href="/leaderboard?rank_by=picks&mode=${mode}">Picks</a></li>
                % endif
                % if rank_by != "bans":
                    <li><a href="/leaderboard?rank_by=bans&mode=${mode}">Bans</a></li>
                % endif
            </ul>

            <li>
                <a class="dropdown-button" data-hover="true" data-beloworigin="true" href="" data-activates="modeDropdown">${mode.title()}<i class="material-icons right">arrow_drop_down</i></a>
            </li>
            <ul id="modeDropdown" class="dropdown-content">
                <li><a href="/daily?rank_by=${rank_by}&mode=${mode}&${getTime(period)}">${mode.title()}</a></li>
                <li class="divider"></li>
                % for m in other_modes:
                    <li><a href="/daily?rank_by=${rank_by}&mode=${m}&${getTime(period)}">${m.title()}</a></li>
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
                    <td class="positionEntry">${i+1} ${progress_arrow(i, player, rank_by) if period == "tournament" else ""}
                    </td>
                    <td class="heroEntry">
                        <a href="${'/profile?user=%s' % player.user_id if mode != 'hero' else ''}">
                        ${player.username}
                        </a>
                    % if len(player_heroes) > i and (not league.transfer_open or league.current_day != period):
                        <span class="hero_images">
                        % for hero in player_heroes[i]:
                            <img src="/static/images/dota/${hero.replace(" ", "_")}_icon.png" title="${hero}" />
                        % endfor
                        </span>
                    %endif
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

<script>
$( document ).ready(function() {
    console.log("ready");
    $(".dropdown-button").dropdown({
        "belowOrigin": true,
        "hover": true
    });

})
</script>
<div id="matchesBlock" class="col s12 m6">
    <div class="card">
    <div class="card-content" id="matchesCard">
        <h2>Matches</h2>
        % for match in match_data:
        <div class="section pointerCursor" id="match-${match['match_id']}">
            <div class="row">
                <!--<img src="/static/images/dota/trophy.png" class=${"hide" if not match["radiant_win"] else ""} />-->
                <span class="radiantTeam">
                    % if match["radiant_win"]:
                    <strong>${match["radiant"]}</strong>
                    % else:
                    ${match["radiant"]}
                    % endif
                </span>
                <span class="direTeam right hide-on-small-only">
                    % if not match["radiant_win"]:
                    <strong>${match["dire"]}</strong>
                    % else:
                    ${match["dire"]}
                    % endif
                </span>
            </div>
            <div class="row" style="margin-bottom: 0px">
                <div class="left">
                    % for hero in match["radiant_picks"]:
                        <span class="${'positive' if hero['points'] >= 0 else 'negative'}" style="display: inline-block; width: 32px; text-align: center;">
                            ${'+' if hero["points"] >= 0 else '-'}${hero["points"]}
                        </span>
                    % endfor
                </div>
                <div class="right hide-on-small-only">
                    % for hero in match["dire_picks"]:
                        <span class="${'positive' if hero['points'] >= 0 else 'negative'}" style="display: inline-block; width: 32px; text-align: center;">
                            ${'+' if hero["points"] >= 0 else '-'}${hero["points"]}
                        </span>
                    % endfor
                </div>
            </div>
            <div class="row">
                <div class="left">
                    % for hero in match["radiant_picks"]:
                        <img src="/static/images/dota/${hero['hero'].replace(' ', '_')}_icon.png" title="${hero['hero']}" />
                    % endfor
                </div>
                <div class="right hide-on-small-only">
                    % for hero in match["dire_picks"]:
                        <img src="/static/images/dota/${hero['hero'].replace(' ', '_')}_icon.png" title="${hero['hero']}"/>
                    % endfor
                </div>
            </div>
            <div class="row" style="margin-bottom: 0px">
                <div class="left">
                    % for hero in match["radiant_bans"]:
                        <img class="banIcon" src="/static/images/dota/${hero['hero'].replace(' ', '_')}_icon.png" title="${hero['hero']}"/>
                    % endfor
                </div>
                <div class="right hide-on-small-only">
                    % for hero in match["dire_bans"]:
                        <img class="banIcon" src="/static/images/dota/${hero['hero'].replace(' ', '_')}_icon.png" title="${hero['hero']}"/>
                    % endfor
                </div>
            </div>
            <div class="row">
                <div class="left">
                    % for hero in match["radiant_bans"]:
                        <span class="${'positive' if hero['points'] >= 0 else 'negative'}" style="display: inline-block; width: 32px; text-align: center;">
                            ${'+' if hero["points"] >= 0 else '-'}${hero["points"]}
                        </span>
                    % endfor
                </div>
                <div class="right hide-on-small-only">
                    % for hero in match["dire_bans"]:
                        <span class="${'positive' if hero['points'] >= 0 else 'negative'}" style="display: inline-block; width: 32px; text-align: center;">
                            ${'+' if hero["points"] >= 0 else '-'}${hero["points"]}
                        </span>
                    % endfor
                </div>
            </div>
            <div name="columniseMobileView show-on-small">
                <div class="row">
                    <span class="direTeam left">
                        % if not match["radiant_win"]:
                        <strong>${match["dire"]}</strong>
                        % else:
                        ${match["dire"]}
                        % endif
                    </span>
                </div>
                <div class="row" style="margin-bottom: 0px">
                    <div class="left">
                        % for hero in match["dire_picks"]:
                            <span class="${'positive' if hero['points'] >= 0 else 'negative'}" style="display: inline-block; width: 32px; text-align: center;">
                                ${'+' if hero["points"] >= 0 else '-'}${hero["points"]}
                            </span>
                        % endfor
                    </div>
                </div>
                <div class="row">
                    <div class="left">
                        % for hero in match["dire_picks"]:
                            <img src="/static/images/dota/${hero['hero'].replace(' ', '_')}_icon.png" title="${hero['hero']}"/>
                        % endfor
                    </div>
                </div>
                <div class="row" style="margin-bottom: 0px">
                    <div class="left">
                        % for hero in match["dire_bans"]:
                            <img class="banIcon" src="/static/images/dota/${hero['hero'].replace(' ', '_')}_icon.png" title="${hero['hero']}"/>
                        % endfor
                    </div>
                </div>
                <div class="row">
                    <div class="left">
                        % for hero in match["dire_bans"]:
                            <span class="${'positive' if hero['points'] >= 0 else 'negative'}" style="display: inline-block; width: 32px; text-align: center;">
                                ${'+' if hero["points"] >= 0 else '-'}${hero["points"]}
                            </span>
                        % endfor
                    </div>
                </div>
            </div>
        </div>
        <div class="divider"></div>
        % endfor

    </div>
    </div>
</div>
</div>
% elif game.code == 'PUBG':
<div class="row">
<div id="leaderboardBlock" class="col s7">
    <nav>
    <div class="nav-wrapper teal darken-2">
        <ul class="left">
            <li class=${"active" if rank_by=="points" else ""}>
                <a id="pointsBtn" href="/daily?rank_by=points&mode=${mode}&${getTime(period)}">
                    Points
                </a>
            </li>
            <li>
                <a class="dropdown-button" data-hover="true" data-beloworigin="true" href="" data-activates="modeDropdown">${mode.title()}<i class="material-icons right">arrow_drop_down</i></a>
            </li>
            <ul id="modeDropdown" class="dropdown-content">
                <li><a href="/daily?rank_by=${rank_by}&mode=${mode}&${getTime(period)}">${mode.title()}</a></li>
                <li class="divider"></li>
                % for m in other_modes:
                    <li><a href="/daily?rank_by=${rank_by}&mode=${m}&${getTime(period)}">${m.title()}</a></li>
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
                    <td class="positionEntry">${i+1} ${progress_arrow(i, player, rank_by) if period == "tournament" else ""}
                    </td>
                    <td class="heroEntry">
                        ${player.username}
                    % if len(player_heroes) > i and (not league.transfer_open or league.current_day != period):
                        <span class="hero_images">
                        % for hero in player_heroes[i]:
                            <img src="/static/images/pubg/teams/${hero.team.replace(" ", "_")}_icon.png" title="${hero.name}" />
                        % endfor
                        </span>
                    %endif
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

<script>
$( document ).ready(function() {
    console.log("ready");
    $(".dropdown-button").dropdown({
        "belowOrigin": true,
        "hover": true
    });

    $(".matchRow").each(function() {
        var elem = $(this)
        var id_ = elem.attr('id');
        var match_id = id_.slice(7)
        elem.click(function() {
            window.open('https://stratz.com/match/' + match_id)
        });
    })
    match-${match['match_id']}

})
</script>
</div>
% endif
