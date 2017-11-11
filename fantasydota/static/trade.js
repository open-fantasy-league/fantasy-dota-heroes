if (!transfers){
    $("[name=buyHero]").add("[name=sellHero]").each(function(){$(this).attr("disabled","true");});
}
else{
    // not sure why but when reloading page...disabled things stay disabled by default :/
    $("[name=buyHero]").add("[name=sellHero]").each(function(){$(this).removeAttr("disabled");})

    function doTrade(event, action){
        var formID = event.data.form.attr('id'),
        tradeUrl = (action == "buyHero") ? "/buyHero" : "/sellHero",
        reserve = parseInt(event.data.form.find('input[name=tradeReserve]').val());
        var formData = {
            "hero": event.data.form.find('input[name=tradeHero]').val(),
            "league": league_id,
            "reserve": reserve,
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
                            reserve ? $("#" + data.hero + "ReserveRow").remove() : $("#" + data.hero + "TeamRow").remove();
                        }
                        else{
                            addToTeam(data.hero, reserve);
                        }
                        reserve ? $(".userReserveCredits").each(function(){$(this).text(data.new_credits)}) : $(".userCredits").each(function(){$(this).text(data.new_credits)});
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
            var value = parseFloat(parent.find(".valueEntry").text());
            doTrade(event, action);
        }

    $(".tradeForm").each(function (){
        var form = $(this);
        var buyBtn = form.find('button[name=buyHero]');
        var sellBtn = form.find('button[name=sellHero]');

        buyBtn.click({form: form}, tradeOnclick);
        sellBtn.click({form: form}, tradeOnclick);
    });

    function addToTeam(hero, reserve){
        var new_row = $("#" + hero + "Row").clone();
        reserve ? new_row.find(".tradeEntry")[0].remove() : new_row.find(".tradeEntry")[1].remove();
        reserve ? new_row.attr('id', hero + "ReserveRow") : new_row.attr('id', hero + "TeamRow");
        new_row.find("button").replaceWith('<button type="submit" name="sellHero" class="btn waves-effect waves-light">Sell</button>');
        var form = new_row.find(".tradeForm");
        var teamRow = reserve ? $(".reserveRow") : $(".teamRow")
        if (teamRow.length != 0) {
            teamRow.last().after(new_row);
        }
        else{
            reserve ? $("#reserveTable").find("tbody").append(new_row) : $("#teamTable").find("tbody").append(new_row);
        }
        new_row.find("button").on("click", {form: form}, function(event){tradeOnclick(event)});  // otherwise need reload page to resell
    }
}

if (!swaps){
    $("[name=swapInHero]").add("[name=swapOutHero]").add("#confirmSwaps").each(function(){$(this).attr("disabled","true");});
}
else{
// not sure why but when reloading page...disabled things stay disabled by default :/
    $("[name=swapInHero]").add("[name=swapOutHero]").add("#confirmSwaps").each(function(){$(this).removeAttr("disabled");})

    function doTrade(event, action){
        var formID = event.data.form.attr('id');
        var tradeUrl = action;
        var formData = {
            "hero": event.data.form.find('input[name=tradeHero]').val(),
            "league": league_id,
        };
        $.ajax({
            url: tradeUrl,
            type: "POST",
            data: formData,
            success: function(data){
                $("[name=swapInHero]").add("[name=swapOutHero]").add("#confirmSwaps").each(function(){$(this).removeAttr("disabled");});
                var success = data.success,
                message = data.message;
                if (!success){
                    sweetAlert(message);
                }
                else{
                    sweetAlert("Transaction completed");
                    if (data.action == "sell"){
                        var toSwap = !$("#" + data.hero + "TeamRow").hasClass('toSwap');
                        $("#" + data.hero + "TeamRow").remove();
                        addToTeam(data.hero, true, toSwap);
//                        var row = $("#" + data.hero + "TeamRow");
//                        row.addClass("activeReserve");
//                        row.find("input[name=tradeReserve]").val(1);
//                        var button = row.find('button');
//                        button.attr('name', 'swapInHero');
//                        button.text('Swap In');
                    }
                    else{
//                        var row = $("#" + data.hero + "TeamRow");
//                        if (row[0]){
//                            row.removeClass("activeReserve");
//                            row.find("input[name=tradeReserve]").val(0);
//                            var button = row.find('button');
//                            button.attr('name', 'swapOutHero');
//                            button.text('Swap Out');
//                        }
//                        else{
                            var toSwap = !$("#" + data.hero + "ReserveRow").hasClass('toSwap');
                            $("#" + data.hero + "ReserveRow").remove();
                            addToTeam(data.hero, false, toSwap);
                    }
                    $(".userCredits").each(function() { $(this).text(data.new_credits)});
                }
            },
            failure: function(data){
                $("[name=swapInHero]").add("[name=swapOutHero]").add("#confirmSwaps").each(function(){$(this).removeAttr("disabled");})
                sweetAlert("Something went wrong. oops!");
            }
        });
    }

    var tradeOnclick = function tradeOnclick(event){
            $("[name=swapInHero]").add("[name=swapOutHero]").add("#confirmSwaps").each(function(){$(this).attr("disabled","true");});
            var action = event.data.form.find('button').attr('name');
            doTrade(event, action);
        }

    $(".tradeForm").each(function (){
        var form = $(this);
        var buyBtn = form.find('button[name=swapInHero]');
        var sellBtn = form.find('button[name=swapOutHero]');

        buyBtn.click({form: form}, tradeOnclick);
        sellBtn.click({form: form}, tradeOnclick);
    });

    function addToTeam(hero, reserve, toSwap){
        var new_row = $("#" + hero + "Row").clone();
        if (toSwap) {
            new_row.addClass('toSwap');
            if (reserve){
                var symbol = "<= ";
                var message = "This hero is set to be swapped out, it will continue to score points until the swap occurs 24 hours after confirmation"
            }
            else{
                var symbol = "=> ";
                var message = "This hero is set to be swapped in, it will not score points until the swap occurs 24 hours after confirmation"
            }
            var name = new_row.find(".heroEntry");
            name.text(symbol + name.text());
            name.attr('title', message);
            name.css('cursor', 'help');
        }
        new_row.find(".tradeEntry")[0].remove();
        reserve ? new_row.attr('id', hero + "ReserveRow") : new_row.attr('id', hero + "TeamRow");
        reserve ? new_row.find("button").replaceWith('<button type="submit" name="swapInHero" class="btn waves-effect waves-light">Swap</button>') :
         new_row.find("button").replaceWith('<button type="submit" name="swapOutHero" class="btn waves-effect waves-light">Swap</button>');
        var form = new_row.find(".tradeForm");
        var teamRow = reserve ? $(".reserveRow") : $(".teamRow")
        if (teamRow.length != 0) {
            teamRow.last().after(new_row);
        }
        else{
            reserve ? $("#reserveTable").find("tbody").append(new_row) : $("#teamTable").find("tbody").append(new_row);
        }
        new_row.find("button").on("click", {form: form}, function(event){tradeOnclick(event)});  // otherwise need reload page to resell
    }

    $('#confirmSwaps').click(function() {
        $("[name=swapInHero]").add("[name=swapOutHero]").add("#confirmSwaps").each(function(){$(this).attr("disabled","true");});
        $.ajax({
            url: "/confirmSwap?league=" + league_id,
            type: "GET",
            success: function(data){
                var success = data.success,
                message = data.message;
                if (!success){
                    sweetAlert(message);
                }
                else{
                    sweetAlert("Swaps locked in! Your active team will update 24 hours from now, at which point you may make further swaps.");
                }
            },
            failure: function(data){
                $("[name=swapInHero]").add("[name=swapOutHero]").each(function(){$(this).removeAttr("disabled");})
                sweetAlert("Something went wrong. oops!");
            }
        });
    });
}

$('.toSwap').each(function(){
    var name = $(this).find(".heroEntry");
    if (name.text()[0] == "<"){
        var message = "This hero is set to be swapped out, it will continue to score points until the swap occurs 24 hours after confirmation"
    }
    else{
        var message = "This hero is set to be swapped in, it will not score points until the swap occurs 24 hours after confirmation"
    }
    name.attr('title', message);
    name.css('cursor', 'help');
})