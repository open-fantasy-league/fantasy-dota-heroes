<%inherit file="layout.mako"/>

<%def name="title()">
    Fantasy DOTA (heroes) Tournament for Boston Major
</%def>

<%def name="meta_keywords()">
    Login, Dota, Fantasy DOTA (heroes)
</%def>

<%def name="meta_description()">
    Login to fantasy dota heroes
</%def>

<div id=${"successMessage" if message and 'have been emailed to you' in message else "message"}>
    % if message:
        ${message}
    % endif
</div>
<div>
    <h2>Existing User</h2>
    <form action="${request.route_path('login')}" method="POST" id="loginForm">
        <input type="text" name="username" placeholder="Username">
        <input type="password" name="password" placeholder="Password">
        <button type="submit">Submit</button>
        <a onclick="forgotPassword()">Forgotten password?</a>
    </form>
</div>

<div>
    <h2>Create Account</h2>
    <form action="${request.route_path('register')}" method="POST" id="createAccountForm">
        <input type="text" name="username" placeholder="Username">
        <br/>
        <input type="text" name="email" placeholder="Email (Optional)">
        <br/>
        <input type="password" name="password" placeholder="Password">
        <input type="password" name="confirm_password" placeholder="Confirm Password">
        <button type="submit">Submit</button>
    </form>
    <ul>
        <li> Email is optional, however necessary to use password reset if you have forgotten yours</li>
        <li> Passwords are encrypted and stored securely </li>
    </ul>
</div>

<script>
function forgotPassword(){
    window.location.href = "/forgotPassword?username=" + $("input[name=username]").val();
}
</script>