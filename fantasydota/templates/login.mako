<%inherit file="layout.mako"/>

<%def name="title()">
    fantasy brood war Heroes
</%def>

<%def name="meta_keywords()">
    Login, Dota, fantasy brood war (heroes)
</%def>

<%def name="meta_description()">
    Login to fantasy brood war heroes
</%def>

<div class="card-panel">
    <div id=${"successMessage" if message and 'have been emailed to you' in message else "message"}>
        % if message:
            ${message}
        % endif
    </div>
</div>
<div class="card">
    <div class="card-content">
        <div class="row">
            <h2><span class="left">Existing User . . .</span>
                <span class="right">... or <a id="steam-button" href="/login/steam/">
                <img src="https://steamcommunity-a.akamaihd.net/public/images/signinthroughsteam/sits_01.png" width="180" height="35" border="0"/>
                </a>
                </span>
            </h2>
        </div>
        <div class="row">
            <form action="${request.route_path('login')}" method="POST" id="loginForm">
                <div class="input-field col s4">
                    <input type="text" name="username" placeholder="Username">
                </div>
                <div class="input-field col s4">
                    <input type="password" name="password" placeholder="Password">
                </div>
                <div class="input-field col s4">
                    <button class="btn waves-effect waves-light" type="submit" name="action">Submit
                    <i class="material-icons right">send</i>
                    </button>
                </div>
                <div class="input-field col s4">
                <a onclick="forgotPassword()" href="#">Forgotten password?</a>
                </div>
            </form>
        </div>
    </div>
</div>

<div class="card">
    <div class="card-content">
        <h2>Create Account</h2>
        <form action="${request.route_path('register')}" method="POST" id="createAccountForm">
        <div class="row">
            <div class="input-field col s4">
            <input type="text" name="username" placeholder="Username">
            </div>
            <div class="input-field col s4">
            <input type="text" name="email" placeholder="Email (Optional)">
            </div>
            <div class="input-field col s4">
            <button class="btn waves-effect waves-light" type="submit" name="action">Submit
                <i class="material-icons right">send</i>
            </button>
            </div>
        </div>
        <div class="row">
            <div class="input-field col s4">
            <input type="password" name="password" placeholder="Password">
            </div>
            <div class="input-field col s4">
            <input type="password" name="confirm_password" placeholder="Confirm Password">
            </div>
        </div>
        </form>
    </div>
</div>

<script>
function forgotPassword(){
    window.location.href = "/forgotPassword?username=" + $("input[name=username]").val();
}
</script>
