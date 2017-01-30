console.log(transfers)
if (!transfers){
    $("[name=buyHero]").add("[name=sellHero]").each(function(){$(this).attr("disabled","true");});
}
else{
    // not sure why but when reloading page...disabled things stay disabled by default :/
    $("[name=buyHero]").add("[name=sellHero]").each(function(){$(this).removeAttr("disabled");})
}

var tradeOnclick = function tradeOnclick(event){
        console.log(event.data.days);
        console.log(event.data.days.val());
        $("[name=buyHero]").add("[name=sellHero]").each(function(){$(this).attr("disabled","true");});
        var formID = event.data.form.attr('id'),
        mode = event.data.mode,
        action = event.data.form.find('button').attr('name'),
        tradeUrlPre = (action == "buyHero") ? "/buyHero" : "/sellHero",
        tradeUrlSuff = (mode == "league") ? "League" : "Bcup",
        formData = {
            "hero": event.data.form.find('input[name=tradeHero]').val(),
            "days": event.data.days.val(),
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
                            (mode == "league") ? addToLeagueTeam(data.hero) : addToTeam(data.hero);
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

$("input[name=days]").each(function () {
    $(this).change(function() {
        var self = $(this)
        var row = self.parent().parent(),
        value = row.find('.valueEntry'),
        adjusted_value = row.find('.adjustedValueEntry');
        var new_val = parseFloat(value.text()) * (1 - (0.015 * (self.val() - 1)));
        adjusted_value.text((Math.round(new_val * 10) / 10).toFixed(1));
        adjusted_value.fadeOut().fadeIn();
    })
})

$(".tradeForm").each(function (){
    var form = $(this);
    var buyBtn = form.find('button[name=buyHero]');
    var sellBtn = form.find('button[name=sellHero]'),
    days = form.parent().parent().find('input[name=days]');

    buyBtn.click({form: form, mode: mode, days: days}, tradeOnclick);
    sellBtn.click({form: form, mode: mode, days: days}, tradeOnclick);
});

function addToTeam(hero){
    var new_row = $("#" + hero + "Row").clone();
    new_row.attr('id', hero + "TeamRow");
    new_row.find("button").replaceWith('<button type="submit" name="sellHero">Sell</button>');
    var form = new_row.find(".tradeForm");
    $("#teamTableTransfers").append(new_row);
    new_row.find("button").on("click", {form: form, mode: mode}, function(event){tradeOnclick(event)});  // otherwise need reload page to resell
}

function addToLeagueTeam(hero){
    var new_row = $("#" + hero + "Row").clone();
    new_row.attr('id', hero + "TeamRow");
    new_row.find("button").replaceWith('<button type="submit" name="sellHero">Cancel loan</button>');
    var days = new_row.find("input[name=days]");
    new_row.find("input[name=days]").replaceWith(days.val());
    var value = new_row.find(".valueEntry");
    value.after('<td class="costEntry">' + value.text() + '</td>');
    var form = new_row.find(".tradeForm");
    $("#teamTableTransfers").append(new_row);
    console.log("days:");
    console.log(days);
    new_row.find("button").on("click", {form: form, mode: mode, days: days}, function(event){tradeOnclick(event)});  // otherwise need reload page to resell
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

// http://stackoverflow.com/a/21323330/3920439
function round2Fixed(value) {
  value = +value;

  if (isNaN(value))
    return NaN;

  // Shift
  value = value.toString().split('e');
  value = Math.round(+(value[0] + 'e' + (value[1] ? (+value[1] + 2) : 2)));

  // Shift back
  value = value.toString().split('e');
  return (+(value[0] + 'e' + (value[1] ? (+value[1] - 2) : -2))).toFixed(2);
}