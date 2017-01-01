<%inherit file="layout.mako"/>

<%def name="title()">
    My Profile
</%def>

<%def name="meta_keywords()">
    Profile, Dota, fantasy, points, game
</%def>

<%def name="meta_description()">
    Profile page for fantasy dota game.
</%def>

<div>
    <h1>League: ${league.name}</h1>
    <p>Hi ${user}</p>
    <span class=${"messageTransOpen" if league.transfer_open else "messageTransClosed"}>
        <p>${"Transfer window currently open. Closes when games start." if league.transfer_open else """Transfer window now closed for tournament. You can still change your battlecup team daily though."""}
        </p>
    </span>
    <span>
    <p>Tables are sortable. Click table headers. Max 5 heroes per team (points penalties for <5)</p>
    </span
</div>

<div id="myTeamBlock">
    <h2>My Team (Total points <span class="teamPoints">${userq.points}</span>)</h2>
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
    <h2>Heroes (Credits Available: <span class="userCredits">${userq.money}</span>)</h2>
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
var transfers = ${'true' if league.transfer_open else 'false'};
if (!transfers){
    $("[name=buyHero]").add("[name=sellHero]").each(function(){$(this).attr("disabled","true");});
}
$(".tradeForm").each(function (){
    var form = $(this);
    var buyBtn = form.find('button[name=buyHero]');
    var sellBtn = form.find('button[name=sellHero]');
    var formID = form.attr('id');

    function tradeOnclick(){
        //$("[name=buyHero]").add("[name=sellHero]").each(function(){$(this).attr("disabled","true");});
        var action = $(this).attr('name'),
        tradeUrl = (action == "buyHero") ? "/buyHeroLeague" : "/sellHeroLeague",
        formData = {
            "hero": form.find('input[name=tradeHero]').val(),
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
                        var heroRow = $("#" + data.hero + "TeamRow");
                        if (data.action == "sell"){
                            heroRow.remove();
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
    buyBtn.click(tradeOnclick);
    sellBtn.click(tradeOnclick);
});
</script>

