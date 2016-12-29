<%inherit file="layout.mako"/>

<%def name="title()">
    Battlecup #${league.current_day + 1} Team: ${league.name}
</%def>

<%def name="meta_keywords()">
    Battlecup, Dota, fantasy, points, game
</%def>

<%def name="meta_description()">
    Battlecup page for fantasy dota game.
</%def>

<script type="text/javascript" src="/static/jquery.bracket.min.js"></script>
<link rel="stylesheet" type="text/css" href="/static/jquery.bracket.min.css" />

<div id="infoBlock" class="row">
    <a href="/previousBattlecups">Previous battlecups</a>
    <p id="message">${"You are not signed up to play in a battlecup. Must have a valid account by the start of the days games" if not is_playing else ""}</p>
    % if len(team) == 0 and transfer_open:
        <p id="message">${"You are not entered in todays battlecup. To do so simply add heroes below"}</p>
    % elif not transfer_open:
        <p id="message">${"Today's battlecup already started. To play tomorrow, add heroes to your battlecup team, between end of matches today, and start of matches tomorrow"}</p>
    %endif
    <p>
    For tied points, winner based on wins, picks, bans in that order (will add 0.1 points to score). </br>
    Hero values in battlecups change each day based on their tournament performance.
    </p>
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
            </tr>
            % for hero in team:
                <tr class="teamRow" id="${hero.id}TeamRow">
                    <td class="heroEntry"><img src="/static/images/${hero.name.replace(" ", "_")}_icon.png"/>
                        ${hero.name}
                    </td>
                    <td class="valueEntry">${hero.value}</td>
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
//RARARARAGAGAGAH WHY DOES THIS BREAK WHEN MOVING TO EXTERNAL FILE!!!!
var transfers = ${'true' if transfer_open else 'false'};
var league_id = ${league.id};

if (!transfers){
    $("[name=buyHero]").add("[name=sellHero]").each(function(){$(this).attr("disabled","true");});
}

var tradeOnclick = function tradeOnclick(event){
        //$("[name=buyHero]").add("[name=sellHero]").each(function(){$(this).attr("disabled","true");});
        console.log(event.data.form);
        var formID = event.data.form.attr('id');
        var action = event.data.form.find('button').attr('name');
        tradeUrl = (action == "buyHero") ? "/buyHeroBcup" : "/sellHeroBcup",
        formData = {
            "hero": event.data.form.find('input[name=tradeHero]').val(),
            "league": ${league.id}
        };
        if (transfers){
            $.ajax({
                url: tradeUrl,
                type: "POST",
                data: formData,
                //contentType: 'application/json',
                success: function(data){
                    //$("[name=buyHero]").add("[name=sellHero]").each(function(){$(this).removeAttr("disabled");});
                    var success = data.success,
                    message = data.message;
                    if (!success){
                        alert(message);
                    }
                    else{
                        alert("Transaction completed");
                        if (data.action == "sell"){
                            $("#" + data.hero + "TeamRow").remove();
                        }
                        else{
                            var new_row = $("#" + data.hero + "Row").clone();
                            new_row.attr('id', data.hero + "TeamRow");
                            new_row.find("button").replaceWith('<button type="submit" name="sellHero">Sell</button>');
                            new_row.find("button").click(tradeOnclick);  // otherwise need reload page to resell
                            $("#teamTable").append(new_row);
                        }
                        $(".userCredits").text(data.new_credits);
                    }
                },
                failure: function(data){
                    $("[name=buyHero]").add("[name=sellHero]").each(function(){$(this).removeAttr("disabled");});
                    alert("Something went wrong. oops!");
                }
            });
        }
    }

$(".tradeForm").each(function (){
    var form = $(this);
    var buyBtn = form.find('button[name=buyHero]');
    var sellBtn = form.find('button[name=sellHero]');
    buyBtn.click({form: form}, tradeOnclick);
    sellBtn.click({form: form}, tradeOnclick);
});

function addToTeam(hero){
    var new_row = $("#" + hero + "Row").clone();
    var form = new_row.find(".tradeForm");
    new_row.attr('id', hero + "TeamRow");
    new_row.find("button").replaceWith('<button type="submit" name="sellHero">Sell</button>');
    new_row.find("button").click({form: form}, tradeOnclick);  // otherwise need reload page to resell
    $("#teamTable").append(new_row);
}

function tryAddGroupHeroes(url){
    if (transfers){
        $.ajax({
            url: url,
            type: "POST",
            data: {"league": league_id},
            dataType: "json",
            success: function(data){
                var success = data.success,
                message = data.message;
                if (!success){
                    alert(message);
                }
                else{
                    alert(data.message);
                    console.log(data.heroes);
                    $("[id*=TeamRow]").each(function(){$(this).remove()});
                    for (i=0; i<data.heroes.length; i++){
                        addToTeam(data.heroes[i]);
                    }
                    $(".userCredits").text(data.new_credits);
                }
            },
            failure: function(data){
                $("[name=buyHero]").add("[name=sellHero]").each(function(){$(this).removeAttr("disabled");});
                alert("Something went wrong. oops!");
            }
        });
    }
}

function tryAddYesterdayHeroes(){
    tryAddGroupHeroes("/bcupTeamAddYesterday");
}

function tryAddLeagueHeroes(){
    tryAddGroupHeroes("/bcupTeamAddLeague");
}

$(".tryAddYesterdayHeroes").click(tryAddYesterdayHeroes);
$(".tryAddLeagueHeroes").click(tryAddLeagueHeroes);
</script>
%endif



% if not transfer_open:

    <div id="battlecupBlock" class="col-md-9">
        <div id="battlecupBracket">
        </div>
    </div>
    <div id="tableContainer" class="col-md-3">
        <table class="sortable" id="heroTable">
            <tr>
                <th class="teamHeader"><h4>Teams</h4></th>
            </tr>
        </table>
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
    console.log(singleElimination1);
        $.ajax({
                url: "/battlecupJson?battlecup_id=${battlecup_id}&league=${league.id}",
                type: "GET",
                //contentType: 'application/json',
                success: function(data){
                    singleElimination = data["bracket_dict"];
                    var hero_imgs = data["hero_imgs"];
                    console.log(singleElimination);
                    $('#battlecupBracket').bracket({
                        init: singleElimination,
                        teamWidth: 200,
                        matchMargin: 100});
                    hero_imgs.forEach(function(element, index){
                        var name = element["pname"],
                        h_imgs = element["heroes"];
                        console.log(index);
                        console.log(h_imgs);
                        if (name != null){
                            var newRow = "<tr class='" + name + "PRow'><td class='playerName'>" + name + "</td><td></td><td></td><td></td></tr>"
                                + "<tr class='listHeroes'>";
                            if (h_imgs.length > 0){
                            for (j=0; j < h_imgs.length; j++){
                                newRow+= "<td class='teamHeroIcon'><img class='heroIcon' src='/static/images/" + h_imgs[j].replace(" ", "_") + "_icon.png' \></td>";
                            }}
                            newRow += "</tr>";
                            $("#heroTable").append(newRow);
                        }
                        $(".blabel").filter(function(index) { return $(this).text() === name; }).hover(function(){
                            var pRow = $("#heroTable").find("." +name + "PRow");
                            pRow.addClass('highlight');
                            pRow.next().addClass('highlight');
                        },
                            function(){
                                var pRow = $("#heroTable").find("." +name + "PRow");
                                pRow.removeClass("highlight");
                                pRow.next().removeClass('highlight');
                            }
                        );
                    })
                    }
                });
    </script>
%endif