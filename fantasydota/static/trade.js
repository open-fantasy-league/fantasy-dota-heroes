var toSell = [];
var toBuy = [];
var wildcard = false;

function disableButtons(){
    $("[name=buyHero]").add("[name=sellHero]").add("#confirmTransfers").add("#useWildcard").each(function(){$(this).attr("disabled","true");});
}

function undisableButtons(){
    $("[name=buyHero]").add("[name=sellHero]").add("#confirmTransfers").add("#useWildcard").each(function(){$(this).removeAttr("disabled");})
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
    swal('Please log in to pick a team!', '', 'error').then(function(){
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
            undisableButtons();
            swal({
             title: "Transfer valid",
             text: "Confirm Transfers to process changes",
              icon: "success",
              timer: 1600
            });
        },
        error: function(jqxhr, textStatus, errorThrown){
            toSell = toSellOriginal;
            toBuy = toBuyOriginal;
            undisableButtons();
            sweetAlert(jqxhr.responseText, '', 'error');
        }
    });
}

function addToTeam(hero, cancel){
    if (cancel){
        var oldRow = $("#" + hero + "TeamRow");
        var btn = oldRow.find("button");
        var heroEntry = oldRow.find(".heroEntry");
        heroEntry.find('i').remove();
        oldRow.removeClass("toTransfer");
        btn.attr('name', 'sellHero');
        btn.text('Sell');
        btn.off('click').click(tradeOnclick);  // otherwise need reload page to resell
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
        btn.off('click').click(tradeOnclick);  // otherwise need reload page to resell
    }
}

function removeFromTeam(hero, cancel){
    console.log("removing from team")
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
        btn.off('click').click(tradeOnclick);  // otherwise need reload page to resell
    }
}
