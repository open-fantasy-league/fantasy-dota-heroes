<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Main page</title>
</head>
<body>
    <%block name="content">
% if request.authenticated_userid is None:
        <a href="${request.route_path('login')}">Login</a>
% else:
        <a href="${request.route_path('logout')}">Logout</a>
% endif
    </%block>
</body>
</html>