<%inherit file="layout.mako"/>

<%def name="title()">
    My Profile
</%def>

<%def name="meta_keywords()">
    Profile, Dota, fantasy, points, game
</%def>

<%def name="meta_description()">
    Profile page for fantasy brood war game.
</%def>

<%!
    def getTopRankingPosition(_user):
        ranks = (("wins", _user.wins_rank, _user.wins), ("points", _user.points_rank, _user.points), ("bans", _user.bans_rank, _user.bans),
            ("picks", _user.picks_rank, _user.picks))
        highest, highest_rank, highest_value = min(ranks, key = lambda x: x[1])
        return highest, highest_rank, highest_value
%>

<div>
    <% top, top_ranking_pos, top_ranking_val = getTopRankingPosition(user) %>
    <p>
    Thanks for playing everyone. Hopefully see you next big tournament for a more improved version!
    </p>
    <p>
    ${"Hi you came 1st for wins/picks/bans. Unfortunately no arcana, however I do have some fall treasure chests for these prizes. please email code 'AdFinemTT' to fantasydotaeu@gmail.com to verify it's you (or just pm me on liquid dota ;) Please provide either steam trade url, or profile link so can add as friend/group to do trade. For trade url go to steam - Trade offers - Who can send me Trade offers" if user.username == "imposer" or user.username == "qoptop" else ""}
    </p>
    <p>
    ${"CONGRATS MR/MRS ARCANA WINNER!!! THANKS FOR PLAYING.  please email code 'AdFinemTT' to fantasydotaeu@gmail.com to verify it's you (or just pm me on liquid dota ;) Please provide either steam trade url, or profile link so can add as friend/group to do trade. For trade url go to steam - Trade offers - Who can send me Trade offers" if user.username == "liquid92" else ""}
    </p>
    <p>Hi ${user.username}. You are currently ranked #${top_ranking_pos} for ${top} with ${top_ranking_val}</p>
    <span class=${"messageTransOpen" if transfer_open else "messageTransClosed"}>
        <p>${"Transfer window currently open. Closes when games start." if transfer_open else """Transfer window currently closed.
        Any transfers made will take place when it re-opens after today's games.
        Heroes that will count towards today's points, but will leave team at end of day are translucent"""}
        </p>
    </span>
    <span>
    <p>Tables are sortable. Click table headers. Max 5 heroes per team (points penalties for <5)</p>
    </span
</div>

<div id="myTeamBlock">
    <h2>My Team (Total points <span class="teamPoints">${user.points}</span>)</h2>
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
            % for hero in [hero_ for hero_ in team if hero_["active"]]:
                <tr class="teamRow ${'toSell' if hero["to_trade"] else ''}" id="${hero["hero_"].hero_id}TeamRow">
                    <td class="heroEntry"><img src="/static/images/${hero["hero_"].name.replace(" ", "_")}_icon.png"/>
                        ${hero["hero_"].name}
                    </td>
                    <td class="valueEntry">${hero["hero_"].value}</td>
                    <td class="heroPointsEntry">${hero["hero_"].points}</td>
                    <td class="picksEntry">${hero["hero_"].picks}</td>
                    <td class="bansEntry">${hero["hero_"].bans}</td>
                    <td class="winsEntry">${hero["hero_"].wins}</td>
                    <td class="tradeEntry">
                        <form name="tradeForm" id="${hero["hero_"].hero_id}TradeForm" class="tradeForm" onsubmit="return false;">
                            <input type="hidden" value="${hero["hero_"].hero_id}" name="tradeHero"/>
                            <button type="submit" name="${'buyHero' if hero["to_trade"] else 'sellHero'}">
                                ${"Buy" if hero["to_trade"] else "Sell"}
                            </button>
                        </form>
                    </td>
                </tr>
            % endfor
        </table>
        <h4>Pending transfers in</h4>
        <table id="teamTableTransfers">
            % for hero in [hero_ for hero_ in team if not hero_["active"]]:
                <tr class="teamRow toBuy" id="${hero["hero_"].hero_id}TeamRow">
                    <td class="heroEntry"><img src="/static/images/${hero["hero_"].name.replace(" ", "_")}_icon.png"/>
                        ${hero["hero_"].name}
                    </td>
                    <td class="valueEntry">${hero["hero_"].value}</td>
                    <td class="heroPointsEntry">${hero["hero_"].points}</td>
                    <td class="picksEntry">${hero["hero_"].picks}</td>
                    <td class="bansEntry">${hero["hero_"].bans}</td>
                    <td class="winsEntry">${hero["hero_"].wins}</td>
                    <td class="tradeEntry">
                        <form name="tradeForm" id="${hero["hero_"].hero_id}TradeForm" class="tradeForm" onsubmit="return false;">
                            <input type="hidden" value="${hero["hero_"].hero_id}" name="tradeHero"/>
                            <button type="submit" name="sellHero">Sell</button>
                        </form>
                    </td>
                </tr>
            % endfor
        </table>
    </div>
    <h2>Heroes (Credits Available: <span class="userCredits">${user.money}</span>)</h2>
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
                <tr id="${hero.hero_id}Row">
                    <td class="heroEntry"><img src="/static/images/${hero.name.replace(" ", "_")}_icon.png"/>${hero.name}</td>
                    <td class="valueEntry">${hero.value}</td>
                    <td class="heroPointsEntry">${hero.points}</td>
                    <td class="picksEntry">${hero.picks}</td>
                    <td class="bansEntry">${hero.bans}</td>
                    <td class="winsEntry">${hero.wins}</td>
                    <td class="tradeEntry">
                        <form name="tradeForm" id="${hero.hero_id}TradeForm" class="tradeForm" onsubmit="return false;">
                            <input type="hidden" value="${hero.hero_id}" name="tradeHero"/>
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
$(".tradeForm").each(function (){
    var form = $(this);
    var buyBtn = form.find('button[name=buyHero]');
    var sellBtn = form.find('button[name=sellHero]');
    var formID = form.attr('id');

    function tradeOnclick(){
        $("[name=buyHero]").add("[name=sellHero]").each(function(){$(this).attr("disabled","true");});
        var action = $(this).attr('name'),
        tradeUrl = (action == "buyHero") ? "/buyHeroLeague" : "/sellHeroLeague",
        formData = {
            "hero": form.find('input[name=tradeHero]').val(),
            "transfer": transfers
        };
        $.ajax({
            url: tradeUrl,
            type: "POST",
            data: formData,
            //contentType: 'application/json',
            success: function(data){
                $("[name=buyHero]").add("[name=sellHero]").each(function(){$(this).removeAttr("disabled");});
                var success = data.success,
                message = data.message;
                if (!success){
                    sweetAlert(message);
                }
                else{
                    sweetAlert("Transaction completed");
                    var heroRow = $("#" + data.hero + "TeamRow");
                    if (data.action == "sell"){
                        if (transfers || (heroRow.attr("class") == "teamRow toBuy")){
                            heroRow.remove();
                        }
                        else{
                            heroRow.attr("class", "teamRow toSell");
                            heroRow.find("button").replaceWith('<button type="submit" name="buyHero">Buy</button>');
                            heroRow.find("button").click(tradeOnclick);
                        }
                    }
                    else{
                        if (heroRow.length > 0){
                            heroRow.attr("class", "teamRow");
                            heroRow.find("button").replaceWith('<button type="submit" name="sellHero">Sell</button>');
                            heroRow.find("button").click(tradeOnclick);
                        }
                        else{
                            if (transfers){
                                var new_row = $("#" + data.hero + "Row").clone();
                                new_row.attr('id', data.hero + "TeamRow");
                                new_row.find("button").replaceWith('<button type="submit" name="sellHero">Sell</button>');
                                new_row.find("button").click(tradeOnclick);  // otherwise need reload page to resell
                                $("#teamTable").append(new_row);
                            }
                            else{
                                var new_row = $("#" + data.hero + "Row").clone();
                                new_row.attr('id', data.hero + "TeamRow");
                                new_row.attr('class', "teamRow toBuy");
                                new_row.find("button").replaceWith('<button type="submit" name="sellHero">Sell</button>');
                                new_row.find("button").click(tradeOnclick);  // otherwise need reload page to resell
                                $("#teamTableTransfers").append(new_row);
                            }
                        }
                    }
                    $(".userCredits").text(data.new_credits);
                }
            },
            failure: function(data){
                $("[name=buyHero]").add("[name=sellHero]").each(function(){$(this).removeAttr("disabled");});
                sweetAlert("Something went wrong. oops!");
            }
        });
    }
    buyBtn.click(tradeOnclick);
    sellBtn.click(tradeOnclick);
});
</script>

