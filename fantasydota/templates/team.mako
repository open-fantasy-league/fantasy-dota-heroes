% if ${game == 'DOTA'}:
    <%namespace name="child" file='league.mako'>
% elif ${game == 'PUBG'}:
    <%namespace name="child" file='team_pubg.mako'>
% else:
    <h1>Invalid game. Please click Dota or Pubg at top</h1>
% endif