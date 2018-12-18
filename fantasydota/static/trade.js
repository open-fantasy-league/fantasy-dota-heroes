var sellCounter = $('i:contains("remove_circle")').length;
if (transferCooldown){
    $("[name=buyHero]").add("[name=sellHero]").add("#confirmTransfers").each(function(){$(this).attr("disabled","true");});
}
else{
    // not sure why but when reloading page...disabled things stay disabled by default :/
    $("[name=buyHero]").add("[name=sellHero]").add("#confirmTransfers").each(function(){$(this).removeAttr("disabled");})
}

function doTrade(event, action, cancel){
    var formID = event.data.form.attr('id'),
    tradeUrl = (action == "buyHero") ? "/buyHero" : "/sellHero";
    var formData = {
        "hero": event.data.form.find('input[name=tradeHero]').val(),
        "league": league_id,
    };
    if (action == "sellHero" && sellCounter >= remainingTransfers){
        swal({
                title: "You do not have sufficient remaining transfers to perform any more changes",
                icon: "error"
            });
    }
    else{
        $.ajax({
            url: tradeUrl,
            type: "POST",
            data: formData,
            success: function(data){
                $("[name=buyHero]").add("[name=sellHero]").each(function(){$(this).removeAttr("disabled");});
                var success = data.success,
                message = data.message;
                if (!success){
                    sweetAlert(message, '', 'error').then(function(){
                        if (data.reload){
                            location.reload();
                        }
                    }
                    );
                }
                else{
                    swal({
                        title: "Transaction completed",
                        icon: "success"
                    });
                    if (data.action == "sell"){
                        removeFromTeam(data.hero, cancel);
                    }
                    else{
                        addToTeam(data.hero, cancel);
                    }
                    $(".userCredits").each(function(){$(this).text(data.new_credits)});
                }
            },
            failure: function(data){
                $("[name=buyHero]").add("[name=sellHero]").each(function(){$(this).removeAttr("disabled");});
                sweetAlert("Something went wrong. oops!", '', 'error');
            }
        });
    }
}

var tradeOnclick = function tradeOnclick(event){
        $("[name=buyHero]").add("[name=sellHero]").each(function(){$(this).attr("disabled","true");});
        console.log(event.data)
        var button = event.data.form.find('button');
        var action = button.attr('name');
        var cancel = button.attr('data-cancel')
        console.log(cancel)
        doTrade(event, action, cancel)
    }

$(".tradeForm").each(function (){
    var form = $(this);
    var buyBtn = form.find('button[name=buyHero]');
    var sellBtn = form.find('button[name=sellHero]');

    buyBtn.click({form: form}, tradeOnclick);
    sellBtn.click({form: form}, tradeOnclick);
});

function addToTeam(hero, cancel){
    if (cancel){
        var oldRow = $("#" + hero + "TeamRow");
        var heroEntry = oldRow.find(".heroEntry");
        heroEntry.find('i').remove();
        oldRow.removeClass("toTransfer");
        oldRow.find("button").replaceWith('<button type="submit" name="sellHero" class="btn waves-effect waves-light">Sell</button>');
        var form = oldRow.find(".tradeForm");
        $("#" + hero + "TeamRow").find("button").on("click", {form: form}, function(event){tradeOnclick(event)});  // otherwise need reload page to resell
        sellCounter = sellCounter - 1;
    }
    else{
        var new_row = $("#" + hero + "Row").clone();
        new_row.attr('id', hero + "TeamRow");
        if (leagueStarted){
            var heroEntry = new_row.find(".heroEntry");
            var plannedSale = heroEntry.find('i');
            heroEntry.prepend('<i class="material-icons">add_circle</i>')
            new_row.addClass("toTransfer");
            new_row.find("button").replaceWith('<button type="submit" name="sellHero" class="btn waves-effect waves-light" data-cancel="data-cancel">Cancel</button>');
        }
        else{
            new_row.find("button").replaceWith('<button type="submit" name="sellHero" class="btn waves-effect waves-light">Sell</button>');
        }
        var form = new_row.find(".tradeForm");
        var teamRow = $(".teamRow")
        if (teamRow.length != 0) {
            teamRow.last().after(new_row);
        }
        else{
            $("#teamTable").find("tbody").append(new_row);
        }
        new_row.find("button").on("click", {form: form}, function(event){tradeOnclick(event)});  // otherwise need reload page to resell
    }
}

function removeFromTeam(hero, cancel){
    if (leagueStarted){
        var oldRow = $("#" + hero + "TeamRow");
        var heroEntry = oldRow.find(".heroEntry");
        if (cancel){
            oldRow.remove()
        }
        else{
            heroEntry.prepend('<i class="material-icons">remove_circle</i>')
            oldRow.addClass("toTransfer");
            oldRow.find("button").replaceWith('<button type="submit" name="buyHero" class="btn waves-effect waves-light" data-cancel="data-cancel">Cancel</button>');
            oldRow.find("button").on("click", {form: oldRow.find('.tradeForm')}, function(event){tradeOnclick(event)});  // otherwise need reload page to resell
            sellCounter = sellCounter + 1;
        }
    }
    else{
        $("#" + hero + "TeamRow").remove();
    }
}

$('#confirmTransfers').click(function() {
    $("[name=buyHero]").add("[name=sellHero]").add("#confirmTransfers").each(function(){$(this).attr("disabled","true");});
    $.ajax({
        url: "/confirmTransfer?league=" + league_id,
        type: "GET",
        success: function(data){
            var success = data.success,
            message = data.message;
            if (!success){
                sweetAlert(message, '', 'error');
            }
            else{
                swal({
                 title: "Transfers locked in!",
                 text: "Note: Your new heroes will start scoring points one hour from now",
                  icon: "success"
                }).then(function(){
                    window.location.reload(false);
                });
            }
        },
        failure: function(data){
            $("[name=buyHero]").add("[name=sellHero]").each(function(){$(this).removeAttr("disabled");})
            sweetAlert("Something went wrong. oops!", '', 'error');
        }
    });
});