<%inherit file="layout.mako"/>

<%def name="title()">
    Winterbot 9000 Drafter
</%def>

<%def name="meta_keywords()">
    Drating AI, Dota
</%def>

<%def name="meta_description()">
    Winterbot 9000 drafting tester.
</%def>

<link rel="stylesheet" href="/static/awesomplete/awesomplete.css" />
<script src="/static/awesomplete/awesomplete.min.js" async></script>

<div class="row" id="myTeamBlock">
    <div class="col s12" id="pickbans">
        <div class="row">
            <div class="col s1">
            </div>
            <h3 class="left">Dire</h3><h3 class="right">Radiant</h3>
        </div>
        % for i in range(20):
            <% is_radiant = (i in [1, 3, 8, 10, 16, 5, 6, 12, 14, 19]) %>
            <% is_pick = (i in [4, 7, 13, 15, 18, 19, 5, 6, 12, 14]) %>
            <div class="divider"></div>
            % if i in [4, 8, 12, 16, 18]:
                <div class="section"></div>
                <div class="divider"></div>
            % endif
            <div class="row" style="margin-bottom:0px">
                <div class="col s1" style="vertical-align:middle; line-height:66px">
                    ${i + 1} <span>${"Pick" if is_pick else "Ban"}</span>
                </div>
                <div class=${"right" if is_radiant else "left"}>
                <input type="text" name="pickban${i}" list="heroes" class="awesomplete"/>
                    <datalist id="heroes">
                        % for h in heroes:
                            <option>${h["name"]}</option>
                        % endfor
                    </datalist>
                </div>
            </div>
        % endfor
    </div>
</div>
<div class="row" id="submitBlock">
    <form name="draftForm" id="draftForm" class="draftForm" onsubmit="return false;">
        <input type="checkbox" class="filled-in" name="useRnn" id="useRnn" checked="checked">
        <label for="useRnn">Use Recurrent Neural Net&nbsp;&nbsp;</label>
        <input type="checkbox" class="filled-in" name="allowDuplicates" id="allowDuplicates">
        <label for="allowDuplicates">Allow Duplicates&nbsp;&nbsp;</label>
        <input type="checkbox" class="filled-in" name="useMax" id="useMax">
        <label for="useMax">Use Max (Always select hero with maximum probability. Rather than making random weighted choice)</label>
        <button type="submit" name="draft" class="btn waves-effect waves-light" id="draftBtn">Draft!</button>
        <button type="submit" name="clear" class="btn waves-effect waves-light" id="clearBtn">Clear</button>
    </form>
    </form>
</div>

<script src="/static/aiform.js"></script>
