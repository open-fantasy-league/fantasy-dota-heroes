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
        <link href="${request.static_url('fantasydota:static/theme.css')}" rel="stylesheet">
        <link href="${request.static_url('fantasydota:static/favicon.ico')}" rel="icon" type="image/x-icon" />

        <!-- Should move these links just to the pages where they belong -->
        <script src="/static/sorttable.js"></script>

        <script src="https://unpkg.com/sweetalert/dist/sweetalert.min.js"></script>
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
            <li id="teamBtn" class="col s1">
                <a href="/team">Team</a>
            </li>
            <li class="col s1">
                <a href="/leaderboard">Leaderboard</a>
            </li>
            <li class="col s1">
                <a href="/daily">Daily</a>
            </li>
                <li class="col s1">
                    <a href="/rules">Rules</a>
                </li>
            </ul>
            <ul class="right hide-on-med-and-down">
                <li><a href="/profile">Profile</a></li>
                <li class="col s2">
                <a class="dropdown-button" data-hover="true" data-beloworigin="true" href="#" data-activates="leagueDropdown">
                    Week
                    <i class="material-icons right">arrow_drop_down</i>
                </a>
                </li>
                    <ul id="leagueDropdown" class="dropdown-content">
                        % for league in leagues:
                        <li><a href="/changeLeague?league=${league.id}">${league.name}</a></li>
                        % endfor
                </ul>
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
                 <li id="leagueBtn" class="col s1">
                    <a href="/team">Team</a>
                </li>
                <li class="col s1">
                    <a href="/leaderboard">Leaderboard</a>
                </li>
                <li class="col s1">
                    <a href="/daily">Daily</a>
                </li>
                <li class="col s1">
                    <a href="/rules">Rules</a>
                </li>
                <div class="divider"></div>
                <li><a href="/profile">Profile</a></li>
                <li class="col s2">
                    <a class="dropdown-button" data-beloworigin="true" href="#" data-activates="mobileLeagueDropdown">
                        Week
                        <i class="material-icons right">arrow_drop_down</i>
                    </a>
                </li>
                <ul id="mobileLeagueDropdown" class="dropdown-content">
                    % for league in leagues:
                    <li><a href="/changeLeague?league=${league.id}">${league.name}</a></li>
                    % endfor
                </ul>
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
        <div class="col s2">
            <a href="/hallOfFame">Hall of Fame</a>
        </div>
                <div>
                     Dota 2 is a registered trademark of Valve Corporation
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
