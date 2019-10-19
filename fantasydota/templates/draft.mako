<%inherit file="layout.mako"/>

<%def name="title()">
    League Team
</%def>

<%def name="meta_keywords()">
    League, Dota, fantasy, points, game
</%def>

<%def name="meta_description()">
    League page for fantasy DotA cards game.
</%def>

<%def name="custom_css()">
</%def>

 <!--
 if draft unstarted first player should be able queue as well
 thin row at top with draft order
big column with available players and stats
two smaller columns with team, and queue
autopick button


scenario where autopick off and has let roll to 60 seconds
schedule at second level,
if time exceeded nextdraft-time check if scheduled pick, also check autopick with queue
rest of the time draft api call has done pick, and reset next-draft-time to future

Constriants for user_ids arrays-->
<div id="draftOrderBlock" class="hide row card-panel"></div>
<div class="row">
    <div id="draftTeamCol" class="col s12 m3">
        <!--<ul id="teamDropdown" class="dropdown-content">
            <li><a>Me</a></li>
            <li class="divider"></li>
        </ul>-->
  <h2>Teams</h2>
  <ul class="collapsible" id="teamsCollapsible">
    <li>
      <div class="collapsible-header"><strong>${username}</strong></div>
      <div class="collapsible-body">
             <table class="card-table striped centered responsive-table" id="teamTable" data-userId="${user_id}"><tbody></tbody>
       </table>
      </div>
    </li>
    % for otherTeam in other_teams:
    <li>
      <div class="collapsible-header">${otherTeam.name}</div>
      <div class="collapsible-body">
             <table class="card-table striped centered responsive-table" class="teamTable" data-userId="${otherTeam.user_id}"><tbody></tbody>
       </table>
      </div>
    </li>
    % endfor
    </ul>
    </div>
    <div id="draftInfoCol" class="col s12 m6">
        <div id="draftUnstartedBlock" class="hide">
        Draft scheduled to start at <span class="draftStartTime"></span>. If you cannot make this time,
        you can pre-select your player queue. Your preferred players will then be auto-drafted for you.
        </div>
        <div id="draftPickeeBlock">
            <table class="sortable card-table striped centered responsive-table" id="pickeeTable">
                <tr style="cursor: pointer" id="teamTableHeader">
                    <th class="draftHeader">Draft</th>
                    <th class="heroHeader">Player</th>
                    <th class="positionHeader">Position</th>
                    <th class="clubHeader">Team</th>
                </tr>
            </table>
        </div>
    </div>
    <div id="draftQueueCol" class="col s12 m3">
        <div class="row">
        </div>

        <div id="draftQueue" class="row">
           <table class="card-table striped centered responsive-table" id="queueTable">
           <thead><tr><th>Queue</th><th colspan="2">        <div class="switch">
            <label>
            Autopick Off
            <input type="checkbox" id="autopickBtn" onchange="switchAutopick(this);" autocomplete="off">
            <span class="lever"></span>
            On
            </label>
        </div></th></tr></thead>
           <tbody></tbody>
           </table>
        </div>
    </div>
</div>

<script src="/static/draft.js?v=1.0"></script>
