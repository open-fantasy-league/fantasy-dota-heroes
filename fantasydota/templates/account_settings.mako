<%inherit file="layout.mako"/>

<%def name="title()">
    Account Settings
</%def>

<%def name="meta_keywords()">
    Account settings, Dota, fantasy, points, game
</%def>

<%def name="meta_description()">
    Account settings page for fantasy dota game.
</%def>

<div>
    % if message:
        <div class="card-panel">
            <div id=${"successMessage" if message_type == 'success' else "message"}>
                ${message}
            </div>
        </div>
    % endif
    <div>
    <h5>Email settings</h5>
        <div class="card-panel">
        <form id="emailSettings" action='/updateEmailSettings'>
            <input type="email" name="email" placeholder="${'Email...' if not user.email else ''}" class="email"
             value=${user.email if user.email else ''}></br>
            Email about upcoming tournaments/news . . .<br>
            <div class="switch">
                <label>
                  Off
                  <input type="checkbox" name="emailContact" ${"checked=checked" if user.contactable else ""}>
                  <span class="lever"></span>
                  On
                </label>
              </div>
            </br>
            <button type="submit" id="change_email_but" class="btn waves-effect waves-light">
                Update email settings</button>
        </form>
        </div>
    </div>


    <div>
    <h5>Update password</h5>
        <div class="card-panel">
        <form id="updatePassword" action='/changePassword'>
            <input type="password" name="old_password" placeholder="Current password" class="pwd">
            <input type="password" name="new_password" placeholder="New password" class="pwd">
            <input type="password" name="confirm_new_password" placeholder="Confirm new password">
            <button type="submit" id="change_pwd_but" class="btn waves-effect waves-light"
            >Change my password</button>
        </form>
        </div>
    </div>
</div>