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

function addToTeam(hero){
    var new_row = $("#" + hero + "Row").clone();
    new_row.attr('id', hero + "TeamRow");
    new_row.find("button").replaceWith('<button type="submit" name="sellHero">Sell</button>');
    new_row.find("button").click(bcupTradeOnclick);  // otherwise need reload page to resell
    $("#teamTable").append(new_row);
}

function tryAddGroupHeroes(url){
    if (transfers){
        $.ajax({
            url: url,
            type: "POST",
            data: {"league": league_id},
            success: function(data){
                var success = data.success,
                message = data.message;
                if (!success){
                    alert(message);
                }
                else{
                    alert("Transaction completed");
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
    tryAddGroupHeroes("/bcupTeamAddYesterday")
}

function tryAddLeagueHeroes(){
    tryAddGroupHeroes("/bcupTeamAddLeague")
}