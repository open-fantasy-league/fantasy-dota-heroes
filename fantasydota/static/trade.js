var toSell = [];
var toBuy = [];

function disableButtons(){
    $("[name=buyHero]").add("[name=sellHero]").add("#confirmTransfers").each(function(){$(this).attr("disabled","true");});
}

function undisableButtons(){
    $("[name=buyHero]").add("[name=sellHero]").add("#confirmTransfers").each(function(){$(this).removeAttr("disabled");})
}

userCanTransfer ? undisableButtons() : disableButtons()

function doTrade(event, action){
    disableButtons();
    var heroId = event.data.attr('data-heroId');
    var cancel = false;
    if (action == "buyHero"){
        if (toSell.contains(heroId)){
            toSell.remove(heroId);
            cancel = true;
        }
        else{
            toBuy.append(heroId)
        }
    }
    else{
        if (toBuy.contains(heroId)){
            toBuy.remove(heroId);
            cancel = true;
        }
        else{
            toSell.append(heroId)
        }
    }
    $.getJson({
        url: apiBaseUrl + "transfers/league" + leagueId + "/user/" + userId,
        type: "POST",
        data: {"toSell": toSell, "toBuy": toBuy, "isCheck": true},
        success: function(data){
            var success = data.success,
            message = data.message;
            if (!success){
                sweetAlert(message, '', 'error');
            }
            else{
                if (data.action == "sell"){
                    removeFromTeam(heroId, cancel);
                }
                else{
                    addToTeam(heroId, cancel);
                }
                $(".userCredits").each(function(){$(this).text(data.new_credits)});
                undisableButtons();
                swal({
                 title: "Transfer valid",
                 text: "Remember to click Confirm Transfers to process changes",
                  icon: "success"
                });
            }
        },
        failure: function(data){
            undisableButtons();
            sweetAlert("Something went wrong. oops!", '', 'error');
        }
    });
}

var tradeOnclick = function tradeOnclick(event){
        disableButtons();
        console.log(event.data)
        var button = $(event.currentTarget);
        var action = button.attr('name');
        doTrade(event, action)
    }

$('button[name=buyHero]').add('button[name=sellHero]').each(function (key, btn){
    btn.click(tradeOnclick);
});

function addToTeam(hero, cancel){
    if (cancel){
        var oldRow = $("#" + hero + "TeamRow");
        var btn = oldRow.find("button");
        var heroEntry = oldRow.find(".heroEntry");
        heroEntry.find('i').remove();
        oldRow.removeClass("toTransfer");
        btn.attr('name', 'sellHero');
        btn.text('Sell');
        btn.on("click", function(event){tradeOnclick(event)});  // otherwise need reload page to resell
    }
    else{
        var new_row = $("#" + hero + "Row").clone();
        new_row.attr('id', hero + "TeamRow");
        var heroEntry = new_row.find(".heroEntry");
        var plannedSale = heroEntry.find('i');
        heroEntry.prepend('<i class="material-icons">add_circle</i>')
        new_row.addClass("toTransfer");
        var btn = new_row.find("button");
        btn.attr('name', 'sellHero');
        btn.text('Cancel');
        var teamRow = $(".teamRow");
        if (teamRow.length != 0) {
            teamRow.last().after(new_row);
        }
        else{
            $("#teamTable").find("tbody").append(new_row);
        }
        btn.on("click", function(event){tradeOnclick(event)});  // otherwise need reload page to resell
    }
}

function removeFromTeam(hero, cancel){
    var oldRow = $("#" + hero + "TeamRow");
    var heroEntry = oldRow.find(".heroEntry");
    if (cancel){
        oldRow.remove();
    }
    else{
        heroEntry.prepend('<i class="material-icons">remove_circle</i>')
        var btn = oldRow.find("button");
        oldRow.addClass("toTransfer");
        btn.attr('name', 'buyHero');
        btn.text('Buy');
        btn.on("click", function(event){tradeOnclick(event)});  // otherwise need reload page to resell
    }
}

$('#confirmTransfers').click(function() {
    disableButtons()
    $.getJson({
        url: apiBaseUrl + "transfers/league" + leagueId + "/user/" + userId,
        type: "POST",
        data: {"toSell": toSell, "toBuy": toBuy, "isCheck": false},
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
            undisableButtons()
            sweetAlert("Something went wrong. oops!", '', 'error');
        }
    });
});