<%inherit file="layout.mako"/>

<%def name="title()">
    % if battlecup:
        Battlecup Day #${battlecup.day + 1} Results: ${league.name}
    % elif transfer_open:
        Battlecup Day #${league.current_day + 1} Team: ${league.name}
    % else:
        Battlecup Day #${league.current_day + 1} Team: ${league.name}
    % endif
</%def>

<%def name="meta_keywords()">
    Battlecup, Dota, fantasy, points, game
</%def>

<%def name="meta_description()">
    Battlecup page for fantasy dota game.
</%def>

<script type="text/javascript" src="/static/jquery.bracket.min.js"></script>
<link rel="stylesheet" type="text/css" href="/static/jquery.bracket.min.css" />

<div class="row">
<nav>
<div class="nav-wrapper purple darken-2">
<ul class="left">
    % for pbcup in reversed(all_bcups):
        <li {class="active if pbcup.id == battlecup.id else ""}>
            % if pbcup.id == battlecup.id:
                <a href="/battlecup?battlecup_id=${pbcup.id}">
            % else:
                <a href="/battlecup?battlecup_id=${pbcup.id}">
            % endif
                % if pbcup.day == league.current_day:
                    Today
                % elif pbcup.day == league.current_day - 1:
                    Yesterday
                % else:
                    Day ${pbcup.day + 1}
                % endif
            </a>
        </li>
    % endfor
</ul>
</div>
</nav>
<div class="card-panel">
<div class="row">
% if len(team) == 0:
    % if transfer_open:
        <p id="message">${"You are not entered in todays battlecup. To do so simply add heroes below"}</p>
    % else:
        <p id="message">${"Today's battlecup already started. To play tomorrow, add heroes to your battlecup team, between end of matches today, and start of matches tomorrow"}</p>
    %endif
% endif
If points are tied, winner based on wins, picks, bans in that order (will add 0.1 points to score). </br>
Hero values in battlecups change each day based on their tournament performance.
</p>
</div>
</div>

% if transfer_open:

<div id="myTeamBlock" class="row">
    <h2>My Battlecup Team</h2>
    <span>
    <p>Tables are sortable. Click table headers. Max 5 heroes per team (points penalties for <5)</p>
    </span>

    <button class="tryAddLeagueHeroes">Select league heroes</button>
    <button class="tryAddYesterdayHeroes">Select yesterdays battlecup heroes</button>
    <div id="tableContainer">
        <table class="sortable" id="teamTable">
            <tr>
                <th class="heroHeader">Hero</th>
                <th class="valueHeader">Value</th>
                <th class="heroPointsHeader">Points</th>
                <th class="picksHeader">Picks</th>
                <th class="bansHeader">Bans</th>
                <th class="winsHeader">Wins</th>
                <th class="sellHeader">Sell</th>
            </tr>
            % for hero in team:
                <tr class="teamRow" id="${hero.id}TeamRow">
                    <td class="heroEntry"><img src="/static/images/${hero.name.replace(" ", "_")}_icon.png"/>
                        ${hero.name}
                    </td>
                    <td class="valueEntry">${hero.value}</td>
                    <td class="heroPointsEntry">${hero.points}</td>
                    <td class="picksEntry">${hero.picks}</td>
                    <td class="bansEntry">${hero.bans}</td>
                    <td class="winsEntry">${hero.wins}</td>
                    <td class="tradeEntry">
                        <form name="tradeForm" id="${hero.id}TradeForm" class="tradeForm" onsubmit="return false;">
                            <input type="hidden" value="${hero.id}" name="tradeHero"/>
                            <button type="submit" name="sellHero">Sell
                            </button>
                        </form>
                    </td>
                </tr>
            % endfor
        </table>
    </div>
</div>
<div class="row">
    <h2>Heroes (Credits Available: <span class="userCredits">${round(50 - (sum([hero.value for hero in team])), 1)}
    </span>)</h2>
    <div id="tableContainer">
        <table class="sortable">
            <tr>
                <th class="heroHeader">Hero</th>
                <th class="valueHeader">Value</th>
                <th class="heroPointsHeader">Points</th>
                <th class="picksHeader">Picks</th>
                <th class="bansHeader">Bans</th>
                <th class="winsHeader">Wins</th>
                <th class="sellHeader">Buy</th>

            </tr>
            % for hero in heroes:
                <tr id="${hero.id}Row">
                    <td class="heroEntry"><img src="/static/images/${hero.name.replace(" ", "_")}_icon.png"/>${hero.name}</td>
                    <td class="valueEntry">${hero.value}</td>
                    <td class="heroPointsEntry">${hero.points}</td>
                    <td class="picksEntry">${hero.picks}</td>
                    <td class="bansEntry">${hero.bans}</td>
                    <td class="winsEntry">${hero.wins}</td>
                    <td class="tradeEntry">
                        <form name="tradeForm" id="${hero.id}TradeForm" class="tradeForm" onsubmit="return false;">
                            <input type="hidden" value="${hero.id}" name="tradeHero"/>
                            <button type="submit" name="buyHero">Buy</button>
                        </form>
                    </td>
                </tr>
            % endfor
        </table>
    </div>
</div>


<script>
var transfers = ${'true' if transfer_open else 'false'};
var league_id = ${league.id};
var mode = "bcup";

</script>

<script src="/static/trade.js"/>
%endif



% if not transfer_open:

    <div id="battlecupBlock" class="col-md-12">
    % if battlecup.day == 0:
        <div class="bcupSeries col-md-3" style="width: 230px; margin-right: 40px">
            <a href="https://www.dotabuff.com/esports/leagues/5018" target="_blank">Group A 1st games</a>
        </div>
        <div class="bcupSeries col-md-3" style="width: 230px; margin-right: 40px">
            <a href="https://www.dotabuff.com/esports/leagues/5018" target="_blank">Group B 1st games</a>
        </div>
        <div class="bcupSeries col-md-3" style="width: 230px; margin-right: 40px">
            <a href="https://www.dotabuff.com/esports/leagues/5018" target="_blank">Group A winners series</a>
        </div>
        <div class="bcupSeries col-md-3" style="width: 230px; margin-right: 40px">
            <a href="https://www.dotabuff.com/esports/leagues/5018" target="_blank">Group B winners series</a>
        </div>
    % elif battlecup.day == 1:
        <div class="bcupSeries col-md-3" style="width: 230px; margin-right: 40px">
            <a href="https://www.dotabuff.com/esports/leagues/5018" target="_blank">Group A losers series</a>
        </div>
        <div class="bcupSeries col-md-3" style="width: 230px; margin-right: 40px">
            <a href="https://www.dotabuff.com/esports/leagues/5018" target="_blank">Group B losers series</a>
        </div>
        <div class="bcupSeries col-md-3" style="width: 230px; margin-right: 40px">
            <a href="https://www.dotabuff.com/esports/leagues/5018" target="_blank">Group A final series</a>
        </div>
        <div class="bcupSeries col-md-3" style="width: 230px; margin-right: 40px">
            <a href="https://www.dotabuff.com/esports/leagues/5018" target="_blank">Group B final series</a>
        </div>
    % endif
        <div id="battlecupBracket">
        </div>
    </div>
    <div id="tableContainer" class="row">
    <div class="col-l-4 col-md-4">
        <table id="heroTable1">
            <tr>
                <th class="teamHeader"></th>
            </tr>
        </table>
    </div>
    <div class="col-l-4 col-md-4">
        <table id="heroTable2">
            <tr>
                <th class="teamHeader"></th>
            </tr>
        </table>
    </div>
    <div class="col-l-4 col-md-4">
        <table id="heroTable3">
            <tr>
                <th class="teamHeader"></th>
            </tr>
        </table>
    </div>
    </div>

    <script>
        var singleElimination;

        // example of data
        var singleElimination1= {
      "teams": [              // Matchups
        ["Team 1", "Team 2"], // First match
        ["Team 3", "Team 4"]  // Second match
      ],
      "results": [            // List of brackets (single elimination, so only one bracket)
        [                     // List of rounds in bracket
          [                   // First round in this bracket
            [1, 2],           // Team 1 vs Team 2
            [3, 4]            // Team 3 vs Team 4
          ],
          [                   // Second (final) round in single elimination bracket
            [5, 6],           // Match for first place
            [7, 8]            // Match for 3rd place
          ]
        ]
      ]
    };
        $.ajax({
                url: "/battlecupJson?battlecup_id=${battlecup.id}&league=${league.id}",
                type: "GET",
                //contentType: 'application/json',
                success: function(data){
                    singleElimination = data["bracket_dict"];
                    var hero_imgs = data["hero_imgs"];
                    console.log(singleElimination);
                    $('#battlecupBracket').bracket({
                        init: singleElimination,
                        teamWidth: 150,
                        matchMargin: 30,
                        roundMargin: 80
                        });
                    var player_count = hero_imgs.length
                    hero_imgs.forEach(function(element, index){
                        var name = element["pname"],
                        h_imgs = element["heroes"];
                        console.log(index);
                        console.log(h_imgs);
                        if (name != null){
                            var newRow = "<tr class='" + name + "PRow listHeroes'><td class='playerName'>" + name + "</td><td class='hero_images'>";
                            if (h_imgs.length > 0){
                            for (j=0; j < h_imgs.length; j++){
                                newRow+= "<img class='heroIcon' src='/static/images/" + h_imgs[j].replace(/ /g, "_") + "_icon.png' \>";
                            }}
                            newRow += "</td></tr>";
                            if (player_count / 3 > index){
                                $("#heroTable1").append(newRow);
                            }
                            else if (2 * player_count / 3 > index){
                                $("#heroTable2").append(newRow);
                            }
                            else{
                                $("#heroTable3").append(newRow);
                            }
                        }
                        $(".blabel").filter(function(index) { return $(this).text() === name; }).hover(function(){
                            var pRow = $("[id*=heroTable]").find("." +name + "PRow");
                            pRow.addClass('myHighlight');
                        },
                            function(){
                                var pRow = $("[id*=heroTable]").find("." +name + "PRow");
                                pRow.removeClass("myHighlight");
                            }
                        );
                    })
                    }
                });
    </script>
%endif