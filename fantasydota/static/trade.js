var toSell = [];
var toBuy = [];
var wildcard = false;
var reversePosOrders = [[0, 'core'], [1, 'offlane'], [2, 'support']];
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
    var cardId = parseInt(button.attr('data-cardid'));
    doTrade(event, action, cardId)
}

var recycleOnClick = function recycleOnClick(event){
    disableButtons();
    var button = $(event.currentTarget);
    var cardId = parseInt(button.attr('data-cardid'));

    $.ajax({
        url: '/recycle_cards',
        dataType: "json",
        contentType: "application/json",
        type: "POST",
        data: JSON.stringify({"cardIds": [cardId]}),
        success: function(data){
            $(".userCredits").each(function(){
                $(this).text(
                        Math.round((parseFloat($(this).text()) + league.recycleValue)*10) / 10)});
            $("#recyclePlayer-" + cardId).parent().parent().parent().remove();
            undisableButtons();
            successClick(button);
        },
        error: function(jqxhr, textStatus, errorThrown){
            undisableButtons();
            Swal.fire({'text': jqxhr.responseJSON.message, 'type': 'error'});
        }
    })
};

var recycleFilteredOnClick = function recycleFilteredOnClick(event){
    disableButtons();
    var toRecycle = $("#cardsContainer > .active").find(".playerCard").not(".hide");
    console.log(toRecycle);
    var toRecycleIds = toRecycle.map(function(){return parseInt(this.dataset.cardid)}).toArray();
    console.log(toRecycleIds);
    Swal.fire({'text': toRecycleIds.length + ' cards will be recycled. Please confirm', showCancelButton: true, 'type': 'info'}).then(function(result){
    if (result.value){
    $.ajax({
        url: '/recycle_cards',
        dataType: "json",

        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({"cardIds": toRecycleIds}),
        success: function(data){
            $(".userCredits").each(function(){
                $(this).text(
                        Math.round((parseFloat($(this).text()) + league.recycleValue * toRecycle.length)*10) / 10)});
            toRecycle.each(function(){this.remove()});
            successClick($(event.currentTarget));
        },
        error: function(jqxhr, textStatus, errorThrown){
            Swal.fire({'text': jqxhr.responseJSON.message, 'type': 'error'});
        }
    })
    }
    undisableButtons();
    })
};

var recycleDupeCommonsOnClick = function recycleDupeCommonsOnClick(event){
    disableButtons();
    var button = $(event.currentTarget);
    var allCards = $(".playerCard");
    var playersToCards = new Map();
    // javascript group by
    allCards.each(function(){
        var card = $(this);
        var player = playersToCards.get(card.attr("data-id"));
        if (player) player.push([card.attr("data-cardid"), card.attr("data-rarity")]);
        else{
        console.log("making new")
            playersToCards.set(card.attr("data-id"), [[card.attr("data-cardid"), card.attr("data-rarity")]]);
        }
    })
    var toRecycleIds = [];
    console.log(playersToCards)
    for (var [key, value] of playersToCards) {
        console.log(value)
        var commons = value.filter(function(a){return a[1] === 'bronze'});
        // If all common slice so as to leave one there
        console.log(commons)
        if (commons.length === value.length){
            commons = commons.slice(1);
        }
        commons.forEach((x) => toRecycleIds.push(x[0]));
    }
    console.log(toRecycleIds)
    if (toRecycleIds.length > 0){
        $.ajax({
            url: '/recycle_cards',
            dataType: "json",
            contentType: "application/json",

            type: "POST",
            data: JSON.stringify({"cardIds": toRecycleIds}),
            success: function(data){
                $(".userCredits").each(function(){
                    $(this).text(
                            Math.round((parseFloat($(this).text()) + league.recycleValue * toRecycleIds.length)*10) / 10)});
                toRecycleIds.forEach((c) => $("div[data-cardid=" + c + "]").remove());
                undisableButtons();
                successClick(button);
            },
            error: function(jqxhr, textStatus, errorThrown){
                undisableButtons();
                Swal.fire({'text': jqxhr.responseJSON.message, 'type': 'error'});
            }
        })
        }
        else{
            Swal.fire({'title': "No Common Duplicates", 'type': 'info'})
        }
};

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
    var isCheck = league.started ? true : false;
    $.ajax({
        url: '/transfer_proxy',
        dataType: "json",

        type: "POST",
        data: {"sell": toSell, "buy": toBuy, "isCheck": isCheck, "wildcard": false},
        success: function(data){
            if (action == "sellPlayer"){
                removeFromTeam(playerId);
            }
            else{
                var playerData = playerDataCache.get(playerId)
                addToTeam(playerData);
            }
            if (!isCheck){
              toSell = [];
              toBuy = [];
            }
            $(".userCredits").each(function(){$(this).text(data.updatedMoney)});
            undisableButtons();
            if (action !== "sellPlayer") successClick($(event.currentTarget));
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
r, j = addPlayerHtmlArray(player, r, j, true);
 return $.parseHTML(r.join(''))
}

function addToTeam(player){
    var new_row = makeTeamRow(player);
    var jnew_row = $(new_row)
    if (showingActive) jnew_row.addClass("hide");
    var btn = jnew_row.find("button");
    var position = player.limitTypes.position;
    var teamRow = $(".teamRow.future." + position);
    var positionRow = $("")
    if (teamRow.length != 0) {
        teamRow.last().after(jnew_row);
    }
    else{
        var currentVal = positionOrder.get(position);
        while (currentVal > -1 && teamRow.length == 0){
            currentVal--;
            var nextPosition = reversePositionOrder.get(currentVal)
            teamRow = $(".teamRow.future" + nextPosition);
        }
        if (teamRow.length != 0){
            teamRow.last().after(jnew_row);
        }
        else{
            $("#teamTable").find("tbody").prepend(jnew_row);
        }
    }
    btn.off('click').click(tradeOnclick);  // otherwise need reload page to resell
}

function removeFromTeam(cardId){
    console.log("removing from team")
    var oldRow = $("#future" + cardId + "TeamRow");
    oldRow.remove();
}
