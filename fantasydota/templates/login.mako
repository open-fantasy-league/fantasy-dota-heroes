<%inherit file="layout.mako"/>

<%def name="title()">
    Fantasy DOTA (heroes) Tournament for Boston Major
</%def>

<%def name="meta_keywords()">
    Login, Dota, stock market
</%def>

<%def name="meta_description()">
    Login to dota stock-market
</%def>

<div id="message">
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
        <li> Please do not forget your password. I have no decent reset system</li>
        <li> Passwords are encrypted and stored securely </li>
        <li> Email is optional, it's not necessary for game. I don't trust small companies/random people with my personal email. Shouldn't expect any difference in reverse.</li>
        <li> Please choose a unique password. The people who get 'hacked' badly usually do so because they have one password across all sites</li>
    </ul>
</div>