getLeagueInfo(false, false, false, false).then(makeLeaderboard);

function makeLeaderboard(){
    var leaderBoardUrl = apiBaseUrl + "leagues/" + leagueId + "/rankings/points" ;
    if (league.currentPeriod){
        leaderBoardUrl = leaderBoardUrl + "?team";
    }
    if (period != 0){
        leaderBoardUrl = leaderBoardUrl + "&period=" + period;
    }
    if (friends.length != 0){
        leaderBoardUrl = leaderBoardUrl + "&users=" + friends.join(",");
    }
    $("#leagueLink").attr('href', league.url);
    $("#leagueLink").text(league.name);
    var r = new Array(), j = -1;
    if (league.currentPeriod){
        for(var i=1; i<=league.currentPeriod.value; i++){
            r[++j] = '<li><a href="/leaderboard?mode=';
            r[++j] = mode;
            r[++j] = "&period=";
            r[++j] = i;
            r[++j] = '">';
            r[++j] = league.periodDescription;
            r[++j] = ' ';
            r[++j] = i;
            r[++j] = '</a></li>';
        }
    }
    $("#periodDropdown").append(r.join(''));
    $.ajax({url: leaderBoardUrl,
                type: "GET",
                dataType: "json",
                success: function(data){
                    var r = new Array(), j = -1;
                    var tfoot = new Array(), k = -1;
                    console.log(data)
                    r[++j] = '<tr><th class="positionHeader">Position</th><th class="teamHeader">Team</th><th class="rankingHeader">';
                    r[++j] = 'Points';
                    r[++j] = '</th></tr>';
                    $.each(data.rankings, function(key, player) {
                        console.log(key)
                        console.log(player)
                        var isUser = (player.id === userId);
                        appendBothUserRows(isUser, r, tfoot, j++, k++,'<tr class="');
                        appendBothUserRows(isUser, r, tfoot, j++, k++, isUser ? 'userRow' : 'playerRow');
                        if (userId != null){
                            tfoot[k++] = ' outsideRanks';
                        }
                        appendBothUserRows(isUser, r, tfoot, j++, k++,'"><td class="positionEntry">');
                        appendBothUserRows(isUser, r, tfoot, j++, k++,player.rank);
                        if (period == 0){
                            appendBothUserRows(isUser, r, tfoot, j++, k++, progress_arrow(player));
                        }
                        appendBothUserRows(isUser, r, tfoot, j++, k++, '</td><td class="teamEntry left"><span style="vertical-align:middle">');
                        if (league.ended && key == 0){
                            r[++j] = '<img src="static/images/dota/trophy.png"/>';
                        }
                        appendBothUserRows(isUser, r, tfoot, j++, k++, player.username);
                        appendBothUserRows(isUser, r, tfoot, j++, k++,'</span><span class="hero_images">');
                        appendBothUserRows(isUser, r, tfoot, j++, k++,'</span></td><td class="rankingHeader">');
                        appendBothUserRows(isUser, r, tfoot, j++, k++,player.value);
                        appendBothUserRows(isUser, r, tfoot, j++, k++,'</td></tr>');
                    })
                    $("#leaderboardTable").find("tbody").html(r.concat(tfoot).join(''));
                },
                error: function(data){
                    Swal.fire("Something went wrong. oops!", '', 'error');
                }
            });
        }

function appendBothUserRows(isUser, r, tfoot, j, k, html){
    r[j] = html;
    if (isUser){
        tfoot[k] = html;
    }
}


function progress_arrow(player){
    if (player.previousRank && friends.length == 0){
        var diff = player.previousRank - player.rank;
        if (diff == 0){
                return " <span>&#8660;</span>";
        }
        else if (diff > 5){
                return ' <span class="upMyArrow">&#8657;</span>';
                }
        else if (diff < -5){
                return ' <span class="downMyArrow">&#8659;</span>';
                }
        else if (diff > 0){
                return ' <span class="supMyArrow">&#8663;</span>';
                }
        else {
                return ' <span class="sdownMyArrow">&#8664;</span>';
        }
    }
    else return '';
}
