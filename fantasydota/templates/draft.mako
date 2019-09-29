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
                    <th class="positionHeader sorttable_numeric">Position</th>
                    <th class="clubHeader sorttable_numeric">Team</th>
                </tr>
                <tbody></tbody>
            </table>
        </div>
    </div>
    <div id="draftQueueCol" class="col s12 m3">
        <div class="row">
        <div class="switch">
            <label>
            Autopick Off
            <input type="checkbox" id="autopickBtn" onchange="switchAutopick(this);" autocomplete="off">
            <span class="lever"></span>
            On
            </label>
        </div>
        </div>

        <div id="draftQueue" class="row">
        </div>
    </div>
</div>

<script src="/static/draft.js?v=1.0"></script>
