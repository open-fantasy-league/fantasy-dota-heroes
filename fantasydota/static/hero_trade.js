var toSell = [];
var toBuy = [];
var wildcard = false;

function disableButtons(){
    $("[name=buyHero]").add("[name=sellHero]").add("#confirmTransfers").add("#useWildcard").each(function(){$(this).attr("disabled","true");});
}

function undisableButtons(){
    $("[name=buyHero]").add("[name=sellHero]").add("#confirmTransfers").add("#useWildcard").each(function(){$(this).removeAttr("disabled");})
}

function undisableButtonsFiltered(money){
    var buyable = $("[name=buyHero][class*=gridHeroBtn]").filter(function() {return parseFloat($(this).text()) <= money;});
    buyable.add("[name=buyHero][class*=tableHeroBtn]").add("[name=sellHero]").add("#confirmTransfers").add("#useWildcard").each(function(){$(this).removeAttr("disabled");})
}

var tradeOnclick = function tradeOnclick(event){
    console.log("tradeonclick")
    disableButtons();
    var button = $(event.currentTarget);
    var action = button.attr('name');
    var heroId = button.attr('data-heroId');
    doTrade(event, action, heroId)
}

var pleaseLogInClick = function pleaseLogInClick(){
    Swal.fire({'title': 'Please log in to pick a team!', 'type': 'error'}).then(function(){
        window.location.href = '/login';
    });
}

function doTrade(event, action, heroId){
    disableButtons();
    var toSellOriginal = toSell.slice();
    var toBuyOriginal = toBuy.slice();
    var cancel = false;
    if (action == "buyHero"){
        var ind = toSell.indexOf(heroId);
        if (ind > -1){
            toSell.splice(ind, 1);
            cancel = true;
        }
        else{
            toBuy.push(heroId)
        }
    }
    else{
        var ind = toBuy.indexOf(heroId);
        if (ind > -1){
            toBuy.splice(ind, 1);
            cancel = true;
        }
        else{
            toSell.push(heroId)
        }
    }
    $.ajax({
        url: '/transfer_proxy',
        dataType: "json",

        type: "POST",
        data: {"sell": toSell, "buy": toBuy, "isCheck": true, "wildcard": wildcard},
        success: function(data){
            if (action == "sellHero"){
                removeFromTeam(heroId, cancel);
            }
            else{
                addToTeam(heroId, cancel);
            }
            $(".userCredits").each(function(){$(this).text(data.updatedMoney)});
            $("#remainingTransfers").text(data.remainingTransfers);
            undisableButtonsFiltered(data.updatedMoney);
            if (action !== "sellHero"){
                successClick($(event.currentTarget));
            }
        },
        error: function(jqxhr, textStatus, errorThrown){
            toSell = toSellOriginal;
            toBuy = toBuyOriginal;
            undisableButtons();
            Swal.fire(jqxhr.responseText, '', 'error');
        }
    });
}

function addToTeam(hero, cancel){
        var new_row = $("#" + hero + "Row").clone();
        new_row.attr("class", "future teamRow");
        if (showingActive) new_row.addClass("hide");
        new_row.attr('id', "future" + hero + "TeamRow");
        var heroEntry = new_row.find(".heroEntry");
        var btn = new_row.find("button");
        btn.attr('name', 'sellHero');
        btn.text('Sell');
        var teamRow = $(".future.teamRow");
        if (teamRow.length != 0) {
            teamRow.last().after(new_row);
        }
        else{
            $("#teamTable").find("tbody").append(new_row);
        }
        btn.off('click').click(tradeOnclick);  // otherwise need reload page to resell
}

function removeFromTeam(hero, cancel){
    console.log("removing from team")
    $("#future" + hero + "TeamRow").remove();
}
