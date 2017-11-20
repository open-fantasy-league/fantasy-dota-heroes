<%inherit file="layout.mako"/>

<%def name="title()">
    Hall of Fame
</%def>

<%def name="meta_keywords()">
    Hall of Fame, Dota, fantasy, points, game
</%def>

<%def name="meta_description()">
    Hall of fame page for fantasy dota game.
</%def>
<div>
    <h2><img src="/static/images/dota/trophy.png"/> Hall of Fame</h2>
</div>
<div>
    % if game_code == 'DOTA':
    <table class="card-table striped">
        <thead>
        <tr>
            <th>Tournament</th>
            <th>League Winner</th>
            <th>Runner-up</th>
        </tr></thead>
        <tbody>
        <tr>
            <td>Boston Major</td>
            <td>Liquid92</td>
            <td>Kattbarn</td>
        </tr>
        <tr>
            <td>ESL Genting</td>
            <td>Nkgrimreaper</td>
            <td>Thepianodentist</td>
        </tr>
        <tr>
            <td>Kiev Major</td>
            <td>Seni</td>
            <td>Noxville</td>
        </tr>
        <tr>
            <td>The International 2017</td>
            <td>Yuridaisuki</td>
            <td>Saranglaba</td>
        </tr>
        <tr>
            <td>ESL Hamburg [Major]</td>
            <td>Liquid92</td>
            <td>JugOrNot</td>
        </tr>
        </tbody>
    </table>
    % elif game_code == 'PUBG':
        <table class="card-table striped">
        <thead>
        <tr>
            <th>Tournament</th>
            <th>League Winner</th>
            <th>Runner-up</th>
        </tr></thead>
        <tbody>
        <tr>
            <td>BEAT Invitational</td>
            <td>Kriger</td>
            <td>WeOwnTheSky</td>
        </tr>
        <tr>
            <td>IEM Oakland Invitational</td>
            <td>Cav</td>
            <td>Lukky96</td>
        </tr>
        </tbody>
    </table>
    %endif

</div>


<div>Trophy Icon made by <a href="http://www.freepik.com" title="Freepik">Freepik</a> from <a href="http://www.flaticon.com" title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>

