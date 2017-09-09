<%! from pyramid.security import authenticated_userid %>

## -*- coding: utf-8 -*-
<!DOCTYPE html>
<html lang="${request.locale_name}">
    <head>
        <meta charset="utf-8">
        <meta name="description" content="${next.meta_description()}">
        <meta name="keywords" content="${next.meta_keywords()}">

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

        <script src="/static/sweetalert.min.js"></script>
        <link rel="stylesheet" type="text/css" href="/static/sweetalert.css">


    </head>

    <body id="mySexyBody" class="blue-grey lighten-5">
        <div id="topBar" class="navbar-fixed">
        <nav>
            <div class="nav-wrapper indigo darken-3">
            <ul class="left">
            <%block name="content">
                % if authenticated_userid(request) is None:
                    <li id="homeLink" class="col s2">
                        <a href="${request.route_path('login')}">Login/Create Profile</a>
                % else:
                    <li><a href="${request.route_path('logout')}">Logout</a></li>
                % endif
            </%block>
            <li id="leagueBtn" class="col s1">
                <a href="/viewLeague">My team</a>
            </li>
            <li class="col s1">
                <a href="/leaderboard">Leaderboard</a>
            </li>
            <li class="col s1">
                <a href="/daily">Daily</a>
            </li>
            </ul>
            <ul class="right">
            <li class="col s1">
                <a href="/rules">Rules</a>
            </li>
            <li class="col s1">
                <a href="/faq">FAQ</a>
            </li>
            <li class="col s2">
                <a href="/hallOfFame">Hall of Fame</a>
            </li>
            <li class="col s3">
                <a href="/accountSettings">Account Settings</a>
            </li>
                <li class="col s3">
                <a href="/guessHero">TI7 Hero Guesser</a>
            </li>
            </ul></div>
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

  </body>
</html>
