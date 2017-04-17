console.log(transfers)
if (!transfers){
    $("[name=buyHero]").add("[name=sellHero]").each(function(){$(this).attr("disabled","true");});
}
else{
    // not sure why but when reloading page...disabled things stay disabled by default :/
    $("[name=buyHero]").add("[name=sellHero]").each(function(){$(this).removeAttr("disabled");})

    function doTrade(event, action){
        var formID = event.data.form.attr('id'),
        tradeUrl = (action == "buyHero") ? "/buyHero" : "/sellHero",
        formData = {
            "hero": event.data.form.find('input[name=tradeHero]').val(),
            "league": league_id
        };
        if (transfers){
            $.ajax({
                url: tradeUrl,
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

    var tradeOnclick = function tradeOnclick(event){
            $("[name=buyHero]").add("[name=sellHero]").each(function(){$(this).attr("disabled","true");});
            var action = event.data.form.find('button').attr('name');
            if (action == "buyHero"){
                doTrade(event, action)
                return
            }
            var parent = event.data.form.parent().parent();
            var cost = parseFloat(parent.find(".costEntry").text());
            var value = parseFloat(parent.find(".valueEntry").text());
            var trade_val = Math.round(((value - cost) * -0.4 + value) * 10) / 10;
            var title = "Confirm trade " + parent.find(".heroEntry").text() + " for " + trade_val + " credits";
            if (trade_val && trade_val != 0 && trade_val != cost){
                sweetAlert({
                    title: title,
                    //text: "for +money credits",
                    type: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "green",
                    cancelButtonColor: "red",
                    confirmButtonText: "Yes!",
                    closeOnConfirm: false },
                    function(isConfirm){
                    if (!isConfirm){
                        $("[name=buyHero]").add("[name=sellHero]").each(function(){$(this).removeAttr("disabled");});
                        return
                    }
                    doTrade(event, action);
                });
            }
            else {
                doTrade(event, action);
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
        new_row.attr('id', hero + "TeamRow");
        new_row.find("button").replaceWith('<button type="submit" name="sellHero" class="btn waves-effect waves-light">Sell</button>');
        var value_box = new_row.find(".valueEntry");
        value_box.after(value_box.clone().attr("class", "costEntry"));
        var form = new_row.find(".tradeForm");
        var teamRow = $(".teamRow")
        if (teamRow.length != 0) {
            $(".teamRow").last().after(new_row);
        }
        else{
            $("#teamTable").find("tbody").append(new_row);
        }
        new_row.find("button").on("click", {form: form}, function(event){tradeOnclick(event)});  // otherwise need reload page to resell
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
}