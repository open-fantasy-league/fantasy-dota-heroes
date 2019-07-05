var toSell = [];
var toBuy = [];
var wildcard = false;
var reversePosOrders = [[0, 'Goalkeeper'], [1, 'Defender'], [2, 'Midfielder'], [3, 'Forward']];
var reversePositionOrder = new Map(reversePosOrders);

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
    var button = $(event.currentTarget);
    var cardId = parseInt(button.attr('data-cardId'));

    $.ajax({
        url: '/recycle_card',
        dataType: "json",

        type: "POST",
        data: {"cardId": cardId},
        success: function(data){
            $(".userCredits").each(function(){$(this).text(data.updatedMoney)});
            $("#recyclePlayer-" + cardId).parent().parent().parent().remove();
            undisableButtons();
            Swal.fire({
             title: "Recycled",
              type: "success",
              timer: 400
            });
        },
        error: function(jqxhr, textStatus, errorThrown){
            undisableButtons();
            Swal.fire({'text': jqxhr.responseText, 'type': 'error'});
        }
    })
}

var pleaseLogInClick = function pleaseLogInClick(){
    Swal.fire('Please log in to pick a team!', '', 'error').then(function(){
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
            Swal.fire({
             title: "Transfer valid",
             text: "Confirm Transfers to process changes",
              type: "success",
              timer: 500
            });
        },
        error: function(jqxhr, textStatus, errorThrown){
            toSell = toSellOriginal;
            toBuy = toBuyOriginal;
            undisableButtons();
            Swal.fire({'text': jqxhr.responseText, 'type': 'error'});
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
    var position = player.limitTypes.position;
    var teamRow = $(".teamRow." + position);
    var positionRow = $("")
    if (teamRow.length != 0) {
        teamRow.last().after(new_row);
    }
    else{
        var currentVal = positionOrder.get(position);
        while (currentVal > -1 && teamRow.length == 0){
            currentVal--;
            var nextPosition = reversePositionOrder.get(currentVal)
            teamRow = $(".teamRow." + nextPosition);
        }
        if (teamRow.length != 0){
            teamRow.last().after(new_row);
        }
        else{
            $("#teamTable").find("tbody").prepend(new_row);
        }
    }
    btn.off('click').click(tradeOnclick);  // otherwise need reload page to resell
}

function removeFromTeam(cardId){
    console.log("removing from team")
    var oldRow = $("#" + cardId + "TeamRow");
    oldRow.remove();
}
