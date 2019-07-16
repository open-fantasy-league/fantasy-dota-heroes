<%! from pyramid.security import authenticated_userid %>
<% user_id = authenticated_userid(request) %>

## -*- coding: utf-8 -*-
<!DOCTYPE html>
<html lang="${request.locale_name}">
    <head>
        <meta charset="utf-8">
        <meta name="description" content="${next.meta_description()}">
        <meta name="keywords" content="${next.meta_keywords()}">
        <meta name="viewport" content="width=device-width">

        <title>${next.title()}</title>

        <link rel="stylesheet" href="//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">
        <!-- Bootstrap core CSS -->
        <script type='text/javascript' src='//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js'></script>

        <!-- Compiled and minified CSS -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.98.0/css/materialize.min.css">

        <!-- Compiled and minified JavaScript -->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.98.0/js/materialize.min.js"></script>
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">


        <!-- Custom styles for this scaffold -->
        <link href="/static/theme.css?v=1.0" rel="stylesheet">
        <link href="/static/favicon.ico?v=1.0" rel="icon" type="image/x-icon" />
        ${next.custom_css()}

        <!-- Should move these links just to the pages where they belong -->
        <script src="/static/thirdparty/sorttable.js"></script>

        <script src="/static/thirdparty/sweetalert2.all.min.js"></script>
        <!--<script src="https://cdn.jsdelivr.net/npm/sweetalert2@8"></script>-->
        <!--<script src="https://cdn.jsdelivr.net/npm/promise-polyfill"></script>-->
        <script>var apiBaseUrl = "${api_base_url}"

            var leagueId = ${league_id};
            var userId = ${user_id if user_id else "null"};
            var username = "${user.username if user else ""}";
            var apiRegistered = ${"true" if api_registered else "false"};
            var league;
            var currentPeriod;
            var getLeagueInfo = function getLeagueInfo(showPeriods, showScoring, showLimits, showStatFields){
                var url = apiBaseUrl + "leagues/" + leagueId + "?";
                if (showPeriods) url = url + "periods&";
                if (showScoring) url = url + "scoring&";
                if (showStatFields) url = url + "statfields&";
                if (showLimits) url = url + "limits&";
                return $.ajax({url: url,
                    dataType: "json",
                    type: "GET",
                    success: function(data){
                        league = data;
                        currentPeriod = league.currentPeriod ? league.currentPeriod.value : 1;
                        var periodLink = $('.periodLink');
                        periodLink.attr('href', "/leaderboard?period=" + currentPeriod);
                        periodLink.text(league.periodDescription);
                        $('.predictionsLink').attr('href', "/predictions?period=" + (league.currentPeriod ? league.currentPeriod.value + 1 : 1));
                    }
                })
            };
            var signup = function signup(){
                if (!apiRegistered){
                $.ajax({url: apiBaseUrl + "users/" + userId + "/join/" + leagueId + "?username=" + username,
                    dataType: "json",
                    type: "POST",
                    data: {"username": username, "userId": userId},
                    success: function(data){
                        console.log("signed up")
                    }
                })
                }
            }
            var posOrders = [['Goalkeeper', 0], ['Defender', 1], ['Midfielder', 2], ['Forward', 3]];
            var positionOrder = new Map(posOrders);
            var positionSort = function positionSort(x, y) {
                        var xval = positionOrder.get(x.limitTypes.position);
                        var yval = positionOrder.get(y.limitTypes.position);
                        if (xval < yval) {
                            return -1;
                        }
                        if (xval > yval) {
                            return 1;
                        }
                            return 0;
                    };

             var positionNameSort = function positionNameSort(x, y) {
                        var xval = positionOrder.get(x.limitTypes.position);
                        var yval = positionOrder.get(y.limitTypes.position);
                        if (xval < yval) {
                            return -1;
                        }
                        if (xval > yval) {
                            return 1;
                        }
                        var x_last = x.name.split(" ").pop();
                        var y_last = y.name.split(" ").pop();
                        if (x_last < y_last) return -1;
                        if (x_last > y_last) return 1;
                        if (x.name < y.name) return -1;
                        if (x.name > y.name) return 1;
                        return 0;
                    };
                    var pleaseLogInClick = function pleaseLogInClick(){
    Swal.fire('<a href="/login">Login to play</a>', '', 'info').then(function(){
        window.location.href = '/login';
    });
}
        </script>

        <!--<script src="/static/sweetalert.min.js"></script>-->
        <!--<link rel="stylesheet" type="text/css" href="/static/sweetalert.css">-->



    </head>

    <body id="mySexyBody" class="blue-grey lighten-5">
    <main>
        <div id="topBar" class="navbar-fixed">
        <nav>
            <div class="nav-wrapper indigo darken-3">
                 <a href="#" data-activates="mobile-nav" class="button-collapse"><i class="material-icons">menu</i></a>
            <ul class="left hide-on-med-and-down">
            <li class="col s1">
                <a class="dropdown-button" data-hover="true" data-beloworigin="true" href="#" data-activates="leagueDropdown">
                    League
                    <i class="material-icons right">arrow_drop_down</i>
                </a>
            </li>
            <ul id="leagueDropdown" class="dropdown-content">
                % for lid, name in leagues.items():
                    <li><a href="/changeLeague?league_id=${lid}">${name}</a></li>
                % endfor
            </ul>
            <li id="teamBtn" class="col s1">
                <a href="/team">Team</a>
            </li>
            <li class="col s1">
                <a href="/predictions" class="predictionsLink">Predictions</a>
            </li>
            <li class="col s1">
                <a href="/leaderboard?period=0">Leaderboard</a>
            </li>
            <li class="col s1">
                <a class="periodLink" href="/leaderboard?period=1">Daily</a>
            </li>
                <li class="col s1">
                    <a href="/rules">Rules</a>
                </li>
            </ul>
            <ul class="right hide-on-med-and-down">
                <li class="col s2">
                    <a href="/collection">Collection</a>
                </li>
                <li class="col s2">
                <a id="notificationButton" class="dropdown-button" data-constrainWidth="false" data-hover="true" data-beloworigin="true" href="#" data-activates="notificationDropdown">
                    Notifications ${"(%s)" % len(notifications)}
                    % if len(notifications) > 1:
                        <i class="material-icons right">arrow_drop_down</i>
                    % endif
                </a>
                </li>
                    <ul id="notificationDropdown" class="dropdown-content">

                        % for i, notification in enumerate(notifications):
                            % if i == 0:
                                <li><a class="clearNotifications center">CLEAR</a></li>
                            % endif
                            <li><span><p>${notification.message}</p></span></li>
                        % endfor
                </ul>
                % if user_id is None:
                    <li id="homeLink" class="col s2">
                        <a href="${request.route_path('login')}">Login/Create Profile</a>
                % else:
                    <li class="col s2">
                    <a class="dropdown-button" data-hover="true" data-beloworigin="true" href="#" data-activates="accountDropdown">
                        Account
                        <i class="material-icons right">arrow_drop_down</i>
                    </a>
                    </li>
                        <ul id="accountDropdown" class="dropdown-content">
                            <li><a href="${request.route_path('logout')}">Logout</a></li>
                            <li><a href="/accountSettings">Settings</a></li>
                        </ul>
                % endif
            </ul>

            <ul class="side-nav" id="mobile-nav">
                <li class="col s1">
                    <a class="dropdown-button" data-hover="true" data-beloworigin="true" href="#" data-activates="mobileLeagueDropdown">
                        League
                        <i class="material-icons right">arrow_drop_down</i>
                    </a>
                </li>
                <ul id="mobileLeagueDropdown" class="dropdown-content">
                    % for lid, name in leagues.items():
                        <li><a href="/changeLeague?league_id=${lid}">${name}</a></li>
                    % endfor
                </ul>
                 <li id="leagueBtn" class="col s1">
                    <a href="/team">Team</a>
                </li>
                <li class="col s1">
                <a href="/predictions" class="predictionsLink">Predictions</a>
            </li>
                <li class="col s1">
                    <a href="/leaderboard?period=0">Leaderboard</a>
                </li>
                <li class="col s1">
                    <a class="periodLink" href="/leaderboard?period=1">Daily</a>
                </li>
                <li class="col s1">
                    <a href="/rules">Rules</a>
                </li>
                <div class="divider"></div>
                                <li class="col s2">
                    <a href="/collection">Collection</a>
                </li>
                <li class="col s2">
                <a id="mobileNotificationButton" class="dropdown-button" data-constrainWidth='false'
                   data-beloworigin="true" href="#" data-activates="mobileNotificationDropdown">
                    Notifications ${"(%s)" % len(notifications)}
                    <i class="material-icons right">arrow_drop_down</i>
                </a>
                </li>
                    <ul id="mobileNotificationDropdown" class="dropdown-content">
                    % for i, notification in enumerate(notifications):
                        % if i == 0:
                            <li><a class="clearNotifications center">CLEAR</a></li>
                        % endif
                        <li><span><p>${notification.message}</p></span></li>
                    % endfor
                </ul>
                % if user_id is None:
                    <li id="homeLink" class="col s2">
                        <a href="${request.route_path('login')}">Login/Create Profile</a>
                    </li>
                % else:
                    <li class="col s2">
                    <a class="dropdown-button" data-beloworigin="true" href="#" data-activates="mobileAccountDropdown">
                        Account
                        <i class="material-icons right">arrow_drop_down</i>
                    </a>
                    </li>
                        <ul id="mobileAccountDropdown" class="dropdown-content">
                            <li><a href="${request.route_path('logout')}">Logout</a></li>
                            <li><a href="/accountSettings">Settings</a></li>
                        </ul>
                % endif
                </ul>
            </div>
        </nav>
        </div>
        <div class="main">
            <div class="container">
        </div>
        <div class="col s12">
            <div class="content">
                <div>
                    <!--<h1><span class="font-semi-bold">${next.title()}</h1>-->
                    <div class="container">
                        ${next.body()}
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
    </main>
    <footer class="page-footer indigo lighten-3">
        <div class="container">
            <div class="row">
        <div class="col s1">
            <a href="/faq">FAQ</a>
        </div>
        <div class="col s1">
            <a href="/privacy">Privacy stuff</a>
        </div>
        <div class="col s2">
            <a href="/hallOfFame">Hall of Fame</a>
        </div>
                <div>
                     This site is 100% unofficial and has no affiliation with the English Premier League, Fotmob, Al-Qaeda or the impending collapse of civilization as we know it.
                     <i>P.S. pls dont sue me.</i>
                </div>
            </div>
        </div>
    </footer>
  </body>

<script>
    function removeOverlay() {
      $('div[id^=sidenav-overlay]').remove();
    }

    $( document ).ready(function(){
      $('.button-collapse').sideNav();
      $('.button-collapse').click(removeOverlay);
      $('.clearNotifications').click(function() {
        $.get('/clearNotifications', function(){window.location.reload(false);});
      });
    })
</script>
</html>
