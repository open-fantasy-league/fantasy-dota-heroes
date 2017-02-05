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

    <body id="mySexyBody">
        <div id="topBar" class="navbar-fixed">
        <nav>
            <div class="nav-wrapper">
            <ul>
            <div id="homeLink" class="col s2">
                <%block name="content">
                    % if request.authenticated_userid is None:
                        <a href="${request.route_path('login')}">Login/Create Profile</a>
                    % else:
                        <a href="${request.route_path('view_index')}">Home /</a>
                        <a href="${request.route_path('logout')}">Logout</a>
                    % endif
                  </%block>
            </div>
            <div id="leagueBtn" class="col s1">
                <a href="${request.route_path('leaderboard')}">League</a>
            </div>
            <div id="battlecupBtn" class="col s1">
                <a href="/battlecup">Battlecups</a>
            </div>
            <div class="col s1">
                <a href="/rules">Rules</a>
            </div>
            <div class="col s1">
                <a href="/faq">FAQ</a>
            </div>
            <div class="col s2">
                <a href="/hallOfFame">Hall of Fame</a>
            </div>
            <div class="col s3">
                <a href="/accountSettings">Account Settings</a>
            </div>
        </div>
        <div class="main blue lighten-5">
            <div class="container">
        </div>
        <div class="col s12">
            <div class="content">
                <div>
                    <h1><span class="font-semi-bold">${next.title()}</h1>
                    <!-- this is where contents of template inheriting from this layout will be inserted -->
                    ${next.body()}
                    <!-- this is where contents of template inheriting from this layout will be inserted -->
                </div>
            </div>
        </div>
    </div>
</div>


    <script>
      (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
      (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
      m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
      })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

      ga('create', 'UA-71035694-1', 'auto');
      ga('send', 'pageview');

    </script>
  </body>
</html>
