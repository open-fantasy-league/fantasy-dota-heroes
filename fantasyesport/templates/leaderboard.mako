<%inherit file="layout.mako"/>

<%def name="title()">
    Leaderboard: ${league.name}
</%def>

<%def name="meta_keywords()">
    Leaderboard, Dota, fantasy, points, game
</%def>

<%def name="meta_description()">
    Leaderboard page for fantasy brood war game.
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
    % endif
</%def>

<%def name="friendOrGlobal(switch_to)">
${"showGlobal=kek" if switch_to == "friend" else "showFriend=kek"}
</%def>

<%def name="getTime(period)">
${"period=%s" % period}
</%def>
<div class="row">
<h2>${rank_by.title()}<a class="right" href="http://wiki.teamliquid.net/starcraft/Afreeca_Team_League_Season_1" target="_blank">${league.name}</a>
</h2>
</div>
<div class="row">
<div id="leaderboardBlock" class="col s7">

    <nav>
    <div class="nav-wrapper teal darken-2">
        <ul class="left">
            <li class=${"active" if rank_by=="points" else ""}>
                <a id="pointsBtn" href="/leaderboard?rank_by=points&${friendOrGlobal(switch_to)}&${getTime(period)}">
                    Points
                </a>
            </li>
            <li class=${"active" if rank_by=="wins" else ""}>
                <a id="winsBtn" href="/leaderboard?rank_by=wins&${friendOrGlobal(switch_to)}&${getTime(period)}">
                    Wins
                </a>
            </li>
            <li class=${"active" if rank_by=="picks" else ""}>
                <a id="picksBtn" href="/leaderboard?rank_by=picks&${friendOrGlobal(switch_to)}&${getTime(period)}">
                    Picks
                </a>
            </li>
            <li><a id="friendsGlobalBtn" href="/leaderboard?rank_by=${rank_by}&${"showFriend=kek" if switch_to == "friend" else "showGlobal=kek"}&${getTime(period)}">
                ${switch_to.title()}
                </a>
            </li>
            <li>
                <a class="dropdown-button" data-beloworigin="true" href="" data-activates="periodDropdown">Period<i class="material-icons right">arrow_drop_down</i></a>
            </li>
            <ul id="periodDropdown" class="dropdown-content">
                <li><a href="/leaderboard?rank_by=${rank_by}&${friendOrGlobal(switch_to)}&period=tournament">Tournament</a></li>
                <li class="divider"></li>
                % for i in range(league.current_day + 1):
                    <li><a href="/leaderboard?rank_by=${rank_by}&${friendOrGlobal(switch_to)}&period=${i}">Round ${i+1}</a></li>
                % endfor
            </ul>
        </ul>
    </div>
    </nav>

    <div id="tableContainer">
        <table id="leaderboardTable" class="card-table">
            <tr>
                <th class="positionHeader">Position</th>
                <th class="playerHeader">Player</th>
                <th class="rankingHeader">${rank_by.title()}</th>
            </tr>
            % for i, player in enumerate(players):
                % if period == "tournament":
                    <tr class=${"playerRow" if not user or player[0].username != user.username else "userRow"}>
                % else:
                    <tr class=${"playerRow" if not user or player[0] != user.username else "userRow"}>
                % endif
                    <td class="positionEntry">${i+1}
                    </td>
                    <td class="heroEntry">${player[0].username if period == "tournament" else player[0]}
                    %if len(player_heroes) > i and not league.transfer_open:
                        <span class="hero_images">
                        % for hero in player_heroes[i]:
                            <img src="/static/images/${hero.replace(" ", "_")}_icon.png"/>
                        % endfor
                        </span>
                    %endif
                    </td>
                    % if period == "tournament":
                        <td class="rankingEntry">${rank_by_fn(rank_by, player[0], False)}</td>
                    % else:
                        <td class="rankingEntry">${rank_by_fn(rank_by, player[1], False)}</td>
                    % endif
                </tr>
            % endfor
            % if user and switch_to == "friend":
                % if period == "tournament":
                    <tr class="userRow outsideRanks">
                        <td class="userRank">${rank_by_fn(rank_by, user, True)}</td>
                        <td class="heroEntry">${user.username}</td>
                        <td class="rankingEntry">${rank_by_fn(rank_by, user, False)}</td>
                    </tr>
                % else:
                    <tr class="userRow outsideRanks">
                        <td class="userRank">${rank_by_fn(rank_by, user[1], True)}</td>
                        <td class="heroEntry">${user[0]}</td>
                        <td class="rankingEntry">${rank_by_fn(rank_by, user[1], False)}</td>
                    </tr>
                % endif
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

% if user:
<div id="friendBlock" class="col s5">
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
    })
    </script>
% else:
    </div>
% endif