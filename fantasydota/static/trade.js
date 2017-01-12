console.log(transfers)
if (!transfers){
    $("[name=buyHero]").add("[name=sellHero]").each(function(){$(this).attr("disabled","true");});
}
else{
    // not sure why but when reloading page...disabled things stay disabled by default :/
    $("[name=buyHero]").add("[name=sellHero]").each(function(){$(this).removeAttr("disabled");})
}

var tradeOnclick = function tradeOnclick(event){
        $("[name=buyHero]").add("[name=sellHero]").each(function(){$(this).attr("disabled","true");});
        var formID = event.data.form.attr('id'),
        mode = event.data.mode,
        action = event.data.form.find('button').attr('name'),
        tradeUrlPre = (action == "buyHero") ? "/buyHero" : "/sellHero",
        tradeUrlSuff = (mode == "league") ? "League" : "Bcup",
        formData = {
            "hero": event.data.form.find('input[name=tradeHero]').val(),
            "league": league_id
        };
        if (transfers){
            $.ajax({
                url: tradeUrlPre + tradeUrlSuff,
                type: "POST",
                data: formData,
                success: function(data){
                    $("[name=buyHero]").add("[name=sellHero]").each(function(){$(this).removeAttr("disabled");});
                    var success = data.success,
                    message = data.message;
                    if (!success){
                        sweetAlert(message);
                    }
                    else{
                        sweetAlert("Transaction completed");
                        if (data.action == "sell"){
                            $("#" + data.hero + "TeamRow").remove();
                        }
                        else{
                            addToTeam(data.hero);
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
    }

$(".tradeForm").each(function (){
    var form = $(this);
    var buyBtn = form.find('button[name=buyHero]');
    var sellBtn = form.find('button[name=sellHero]');
    buyBtn.click({form: form, mode: mode}, tradeOnclick);
    sellBtn.click({form: form, mode: mode}, tradeOnclick);
});

function addToTeam(hero){
    var new_row = $("#" + hero + "Row").clone();
    new_row.attr('id', hero + "TeamRow");
    new_row.find("button").replaceWith('<button type="submit" name="sellHero">Sell</button>');
    var form = new_row.find(".tradeForm")
    $("#teamTable").append(new_row);
    new_row.find("button").on("click", {form: form, mode: mode}, function(event){tradeOnclick(event)});  // otherwise need reload page to resell
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
                    sweetAlert(message);
                }
                else{
                    sweetAlert(data.message);
                    $("[id*=TeamRow]").each(function(){$(this).remove()});
                    for (i=0; i<data.heroes.length; i++){
                        addToTeam(data.heroes[i]);
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
}

function tryAddYesterdayHeroes(){
    tryAddGroupHeroes("/bcupTeamAddYesterday");
}

function tryAddLeagueHeroes(){
    tryAddGroupHeroes("/bcupTeamAddLeague");
}

if (mode != "league"){
    $(".tryAddYesterdayHeroes").click(tryAddYesterdayHeroes);
    $(".tryAddLeagueHeroes").click(tryAddLeagueHeroes);
}