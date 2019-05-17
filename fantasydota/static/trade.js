var toSell = [];
var toBuy = [];
var wildcard = false;

function disableButtons(){
    $("[name=buyPlayer]").add("[name=sellPlayer]").add("#confirmTransfers").each(function(){$(this).attr("disabled","true");});
}

function undisableButtons(){
    $("[name=buyPlayer]").add("[name=sellPlayer]").add("#confirmTransfers").each(function(){$(this).removeAttr("disabled");})
}

function undisableButtonsFiltered(money){
    var buyable = $("[name=buyPlayer][class*=gridPlayerBtn]").filter(function() {return parseFloat($(this).text()) <= money;});
    buyable.add("[name=buyPlayer][class*=tablePlayerBtn]").add("[name=sellPlayer]").add("#confirmTransfers").add("#useWildcard").each(function(){$(this).removeAttr("disabled");})
}

var tradeOnclick = function tradeOnclick(event){
    console.log("tradeonclick")
    disableButtons();
    var button = $(event.currentTarget);
    var action = button.attr('name');
    var cardId = parseInt(button.attr('data-cardId'));
    doTrade(event, action, cardId)
}

var recycleOnClick = function recycleOnClick(event){
    var cardId = parseInt(button.attr('data-cardId'));

    $.ajax({
        url: '/recycle_card',
        dataType: "json",

        type: "POST",
        data: {"cardId": cardId},
        success: function(data){
            $(".userCredits").each(function(){$(this).text(data.updatedMoney)});
            $(".playerCard") > child$("#recyclePlayer-" + cardId).remove();
            undisableButtons();
            swal({
             title: "Recycled",
              icon: "success",
              timer: 400
            });
        },
        error: function(jqxhr, textStatus, errorThrown){
            undisableButtons();
            sweetAlert(jqxhr.responseText, '', 'error');
        }
    })
}

var pleaseLogInClick = function pleaseLogInClick(){
    swal('Please log in to pick a team!', '', 'error').then(function(){
        window.location.href = '/login';
    });
}

function doTrade(event, action, playerId){
console.log(playerId)
    disableButtons();
    var toSellOriginal = toSell.slice();
    var toBuyOriginal = toBuy.slice();
    if (action == "buyPlayer"){
        var ind = toSell.indexOf(playerId);
        if (ind > -1){
            toSell.splice(ind, 1);
        }
        else{
            toBuy.push(playerId)
        }
    }
    else{
        var ind = toBuy.indexOf(playerId);
        if (ind > -1){
            toBuy.splice(ind, 1);
        }
        else{
            toSell.push(playerId)
            console.log(toSell)
        }
    }
    $.ajax({
        url: '/transfer_proxy',
        dataType: "json",

        type: "POST",
        data: {"sell": toSell, "buy": toBuy, "isCheck": true, "wildcard": false},
        success: function(data){
            if (action == "sellPlayer"){
                removeFromTeam(playerId);
            }
            else{
                var playerData = playerDataCache.get(playerId)
                addToTeam(playerData);
            }
            $(".userCredits").each(function(){$(this).text(data.updatedMoney)});
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

function makeTeamRow(player){
var r = new Array(), j = -1;
r, j = addPlayerHtmlArray(player, r, j);
 return $.parseHTML(r.join(''))
}

function addToTeam(player){
    var new_row = makeTeamRow(player);
    var btn = $(new_row).find("button");
    var teamRow = $(".teamRow");
    if (teamRow.length != 0) {
        teamRow.last().after(new_row);
    }
    else{
        $("#teamTable").find("tbody").append(new_row);
    }
    btn.off('click').click(tradeOnclick);  // otherwise need reload page to resell
}

function removeFromTeam(cardId){
    console.log("removing from team")
    var oldRow = $("#" + cardId + "TeamRow");
    oldRow.remove();
}
