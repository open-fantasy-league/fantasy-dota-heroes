<%inherit file="layout.mako"/>

<%def name="title()">
    Password reset
</%def>

<%def name="meta_keywords()">
    Password reset, Dota, fantasy, points, game
</%def>

<%def name="meta_description()">
    Password reset page for fantasy dota game.
</%def>
% if message:
    <div class="card-panel">
        <div id=${"successMessage" if message and 'have been emailed to you' in message else "message"}>
            % if message:
                ${message}
            % endif
        </div>
    </div>
% endif
<div class="card">
    <div class="card-content">
        <div class="row">
            <h2>Recover Password
            </h2>
        </div>
        <div class="row">
            <form action="${request.route_path('forgot_password')}" method="POST" id="recoverPasswordForm">
                <div class="input-field col s4">
                    <input type="text" name="username" placeholder="Username">
                </div>
                <div class="input-field col s4">
                    <input type="email" name="email" placeholder="Email">
                </div>
                <div class="input-field col s4">
                    <button class="btn waves-effect waves-light" type="submit" name="action">Submit
                    <i class="material-icons right">send</i>
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>