<%inherit file="layout.mako"/>

<%def name="title()">
    Leaderboards
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
            ${round(player.points, 1)}
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

<%def name="friendOrGlobal(switch_to)">
${"showGlobal=kek" if switch_to == "friend" else "showFriend=kek"}
</%def>

<%def name="getTime(period)">
${"period=%s" % period}
</%def>

<div id="leaderboardBlock" class="col-md-7">
    Players chosen heroes will be shown only whilst transfer window closed. Points updated hourly.
    <h2>${rank_by.title()}</h2>
    <div>
        <ul class="w3-navbar w3-border-bottom w3-light-grey intronav">
            <li>
                <a id="pointsBtn" href="/leaderboard?rank_by=points&${friendOrGlobal(switch_to)}&${getTime(period)}" class=${"w3-dark-grey" if rank_by=="points" else ""}>
                    Points
                </a>
            </li>
            <li>
                <a id="winsBtn" href="/leaderboard?rank_by=wins&${friendOrGlobal(switch_to)}&${getTime(period)}" class=${"w3-dark-grey" if rank_by=="wins" else ""}>
                    Wins
                </a>
            </li>
            <li>
                <a id="picksBtn" href="/leaderboard?rank_by=picks&${friendOrGlobal(switch_to)}&${getTime(period)}" class=${"w3-dark-grey" if rank_by=="picks" else ""}>
                    Picks
                </a>
            </li>
            <li>
                <a id="bansBtn" href="/leaderboard?rank_by=bans&${friendOrGlobal(switch_to)}&${getTime(period)}" class=${"w3-dark-grey" if rank_by=="bans" else ""}>
                    Bans
                </a>
            </li>
            <li><a id="friendsGlobalBtn" href="/leaderboard?rank_by=${rank_by}&${"showFriend=kek" if switch_to == "friend" else "showGlobal=kek"}&${getTime(period)}">
                ${switch_to.title()}
                </a>
            </li>
            <li class="w3-dropdown-hover">
                <a>Period</a>
                <div class="w3-dropdown-content w3-border">
                    <a href="/leaderboard?rank_by=${rank_by}&${friendOrGlobal(switch_to)}&period=tournament">Tournament</a>
                    <a href="/leaderboard?rank_by=${rank_by}&${friendOrGlobal(switch_to)}&period=day1">Day 1</a>
                    <a href="/leaderboard?rank_by=${rank_by}&${friendOrGlobal(switch_to)}&period=day2">Day 2</a>
                    <a href="/leaderboard?rank_by=${rank_by}&${friendOrGlobal(switch_to)}&period=day3">Day 3</a>
		            <a href="/leaderboard?rank_by=${rank_by}&${friendOrGlobal(switch_to)}&period=day4">Day 4</a>
		            <a href="/leaderboard?rank_by=${rank_by}&${friendOrGlobal(switch_to)}&period=day5">Day 5</a>
		            <a href="/leaderboard?rank_by=${rank_by}&${friendOrGlobal(switch_to)}&period=day6">Finals</a>
	</div>
            </li>
        </ul>
    </div>
    <div id="tableContainer">
        <table id="leaderboardTable">
            <tr>
                <th class="positionHeader">Position</th>
                <th class="playerHeader">Player</th>
                <th class="rankingHeader">${rank_by.title()}</th>
            </tr>
            % for i, player in enumerate(players):
                <tr class=${"playerRow" if not user or player.username != user.username else "userRow"}>
                    <td class="positionEntry">${i+1}
                    </td>
                    <td class="heroEntry">${player.username}
                    %if len(player_heroes) > i:
                        <span class="hero_images_leaderboard">
                        % for hero in player_heroes[i]:
                            <img src="/static/images/${hero.replace(" ", "_")}_icon.png"/>
                        % endfor
                        </span>
                    %endif
                    </td>
                    <td class="rankingEntry">${rank_by_fn(rank_by, player, False)}</td>
                </tr>
            % endfor
            % if user:
            <tr class="userRow outsideRanks">
                <td class="userRank">${rank_by_fn(rank_by, user, True)}</td>
                <td class="heroEntry">${user.username}</td>
                <td class="rankingEntry">${rank_by_fn(rank_by, user, False)}</td>
            </tr>
            % endif
        </table>
    </div>
    <div>Trophy Icon made by <a href="http://www.freepik.com" title="Freepik">Freepik</a> from <a href="http://www.flaticon.com" title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>
</div>

% if user:
    <div id="friendBlock" class="col-md-5">
        <p>
            Add friends usernames to compete in tables versus them
        </p>
        <form name="addFriendForm" onsubmit="return false;">
            <input type="text" name="newFriend" placeholder="New friend..."/>
            <button type="button" id="addFriendBtn">Add</button>
        </form>
    </div>

    <script>
    function addFriendOnclick(){
        $.ajax({
                url: "/addFriend",
                type: "POST",
                data: {"newFriend": $("input[name=newFriend]").val()},
                success: function(data){
                    var success = data.success,
                    message = data.message;
                    if (!success){
                        alert(message);
                    }
                    else{
                        window.location.reload();
                    }
                }
            }
        );
    };
    $("#addFriendBtn").click(addFriendOnclick);
    </script>
% endif