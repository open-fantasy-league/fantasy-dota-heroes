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

<%def name="custom_css()">
</%def>

<div>
    <div>
    <h5>Password Reset</h5>
        <form id="updatePassword" action='/resetPassword'>
            <input type="hidden" name="guid" value="${guid}"/>
            <input type="hidden" name="user_id" value="${user_id}"/>
            <input type="password" name="new_password" placeholder="New password" class="pwd">
            <input type="password" name="confirm_new_password" placeholder="Confirm new password">
            <button type="submit" id="change_pwd_but">Reset my password</button>
        </form>
    </div>
</div>