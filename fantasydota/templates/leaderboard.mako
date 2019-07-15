<%inherit file="layout.mako"/>

<%def name="title()">
    Leaderboard
</%def>

<%def name="meta_keywords()">
    Leaderboard, Dota, fantasy, points, game
</%def>

<%def name="meta_description()">
    Leaderboard page for fantasy DotA cards game.
</%def>

<%def name="custom_css()">
</%def>

<div class="row">
    <h2>${"Tournament: Points" if period == 0 else "Day {}: Points".format(period)}
        <a class="right" id="leagueLink" target="_blank"></a></h2>
</div>
<div class="row">
<div id="leaderboardBlock" class="col m7 s12">
    <nav>
    <div class="nav-wrapper teal darken-2">
        <ul class="left">
            <li>
                <a class="dropdown-button leaderboardDropdown" data-hover="true" data-beloworigin="true" href="" data-activates="modeDropdown">${mode.title()}<i class="material-icons right">arrow_drop_down</i></a>
            </li>
            <ul id="modeDropdown" class="dropdown-content">
                <li><a href="/leaderboard?mode=${mode}&period=${period}">${mode.title()}</a></li>
                <li class="divider"></li>
                % for m in other_modes:
                    <li><a href="/leaderboard?mode=${m}&period=${period}">${m.title()}</a></li>
                % endfor
            </ul>
            <li>
                <a class="dropdown-button leaderboardDropdown" data-hover="true" data-beloworigin="true" href="" data-activates="periodDropdown">Period<i class="material-icons right">arrow_drop_down</i></a>
            </li>
            <ul id="periodDropdown" class="dropdown-content">
                <li><a href="/leaderboard?mode=${mode}&period=0">Tournament</a></li>
                <li class="divider"></li>
            </ul>
        </ul>
    </div>
    </nav>

    <div id="tableContainer">
        <table id="leaderboardTable" class="card-table striped centered">
            <tbody></tbody>
        </table>
    </div>
</div>

<script>
var mode = "${mode}";
var period = ${period};
var friends = ${friends};

$( document ).ready(function() {
    $(".dropdown-button").dropdown({
        "belowOrigin": true,
        "hover": true
    });
})
</script>
    <script src="/static/leaderboard.js?v=1.1"></script>
    <div id="friendBlock" class="col s12 m5">
        <div class="card-panel">
        <p>2x points multiplier for final day</p>
            <p>Results updated end of match day</p>
            <p><a href="https://discord.gg/MAH7EEv" target="_blank">Discord channel for suggestions/improvements</a></p>
        </div>
    % if user_id:
        <div class="card">
        <div class="card-content">
            <p>
                Add friends usernames to compete in tables just against them
            </p>
            <form name="addFriendForm" onsubmit="return false;">
                <input type="text" name="newFriend" placeholder="New friend..."/>
                <button type="submit" id="addFriendBtn" class="btn waves-effect waves-light">Add</button>
            </form>
        </div>
        </div>
        <script>
    $( document ).ready(function() {
        //$(".dropdown-button").dropdown({"hover": true});
        function addFriendOnclick(){
            $.ajax({
                    url: "/addFriend",
                    type: "POST",
                    data: {"newFriend": $("input[name=newFriend]").val()},
                    success: function(data){
                        var success = data.success,
                        message = data.message;
                        if (!success){
                            Swal.fire(message);
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
        % endif
</div>
</div>
