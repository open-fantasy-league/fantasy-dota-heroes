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
Will add this soon.

Functionality to update password. Also to remove account
    <div>
    <h5>Email settings</h5>
        <form id="emailSettings" action='/change_password'>
            <input type="password" name="old_password" placeholder="Current password" class="pwd">
            <input type="email" name="email" placeholder="Email" class="email">
            <input type="checkbox" name="emailContact">Can we email you about upcoming tournaments?<br>
            <button type="submit" id="change_email_but">Update email settings</button>
        </form>
    </div>


    <div>
    <h5>Update password</h5>
        <form id="updatePassword" action='/changePassword'>
            <input type="password" name="old_password" placeholder="Current password" class="pwd">
            <input type="password" name="new_password" placeholder="New password" class="pwd">
            <input type="password" name="confirm_new_password" placeholder="Confirm new password">
            <button type="submit" id="change_pwd_but">Change my password</button>
        </form>
    </div>

    <div>
    <h5>Permanently delete account</h5>
        <form id="deleteAccount" action='/delete_account'>
            <button type="submit" id="delete_account_but">Delete My Account (Will be removed at midnight)</button>
        </form>
    </div>
</div>