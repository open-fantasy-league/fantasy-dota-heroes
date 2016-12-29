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
    <div>
    <h5>Email settings</h5>
        <form id="emailSettings" action='/updateEmailSettings'>
            <input type="email" name="email" placeholder="${user.email if user.email else 'Email...'}" class="email"></br>
            <input type="checkbox" name="emailContact" ${"checked" if user.contactable else ""}>
            Do you want emailing about upcoming tournaments/news?<br>
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
</div>