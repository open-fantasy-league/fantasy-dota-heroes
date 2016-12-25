## -*- coding: utf-8 -*-
<!DOCTYPE html>
<html lang="${request.locale_name}">
  <head>
    <meta charset="utf-8">
    <meta name="description" content="${next.meta_description()}">
    <meta name="keywords" content="${next.meta_keywords()}">

    <title>${next.title()}</title>

    <link rel="stylesheet" href="//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">
    <!-- Should move these links just to the pages where they belong.but if this loaded after bootstrap
     it looks shit lol-->
    <link rel="stylesheet" href="/static/w3.css">
    <!-- Bootstrap core CSS -->
    <link href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">
    <script type='text/javascript' src='//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js'></script>
    <script type='text/javascript' src='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js'></script>

    <!-- Custom styles for this scaffold -->
    <link href="${request.static_url('fantasydota:static/theme.css')}" rel="stylesheet">
    <link href="${request.static_url('fantasydota:static/favicon.ico')}" rel="icon" type="image/x-icon" />

    <!-- Should move these links just to the pages where they belong -->
    <script src="/static/sorttable.js"></script>


  </head>

  <body id="mySexyBody">
  <div class="container">
    <div id="topBar" class="row">
      <div id="homeLink" class="col-lg-1 col-md-1 col-sm-1 col-xs-1">
        <a href="/">Home</a>
      </div>
      <div id="loginStuff" class="col-lg-2 col-md-2 col-sm-2 col-xs-2">
          <%block name="content">
            % if request.authenticated_userid is None:
                    <a href="${request.route_path('login')}">Login/Create Profile</a>
            % else:
                    <a href="${request.route_path('view_account')}">League /</a>
                    <a href="${request.route_path('logout')}">Logout</a>
            % endif
          </%block>
      </div>
      <div id="leaderboardBtn" class="col-lg-2 col-md-2 col-sm-2 col-xs-2">
        <a href="/leaderboard?rank_by=points">Leaderboards</a>
      </div>
      <div id="battlecupBtn" class="col-lg-1 col-md-1 col-sm-1 col-xs-1">
        <a href="/battlecup">Battlecup</a>
      </div>
      <div class="col-lg-1 col-md-1 col-sm-1 col-xs-1">
        <a href="/news">News</a>
      </div>
      <div class="col-lg-1 col-md-1 col-sm-1 col-xs-1">
        <a href="/rules">Rules</a>
      </div>
      <div class="col-lg-1 col-md-1 col-sm-1 col-xs-1">
        <a href="/faq">FAQ</a>
      </div>

      <div class="col-lg-3 col-md-3 col-sm-1 col-xs-1">
        <a href="/accountSettings">Account Settings</a>
      </div>
    </div>
    <div class="row">
      <div class="col-md-12">
        <div class="content">
          <h1><span class="font-semi-bold">${next.title()}</h1>
            <div>
                <!-- this is where contents of template inheriting from this layout will be inserted -->
              ${next.body()}
                <!-- this is where contents of template inheriting from this layout will be inserted -->
            </div>

        </div>
      </div>
    </div>
  </div>



    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="//oss.maxcdn.com/libs/twitter-bootstrap/3.0.3/js/bootstrap.min.js"></script>
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
