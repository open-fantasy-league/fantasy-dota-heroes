## -*- coding: utf-8 -*-
<%inherit file="tutorial:templates/layout.mako"/>

<%def name="title()">
    SEO Rank - ${search_info.search} - ${location}
</%def>

<%def name="meta_keywords()">
    table, SEO, rank, ${search_info.search}
</%def>

<%def name="meta_description()">
    Table displaying rankings for ${search_info.search} from ${location} at google search
</%def>

<%def name="hasEntry()">
  <%
    return hasEntry
  %>
</%def>

<% link_attr={"class": "btn btn-default btn-xs"} %>
<% curpage_attr={"class": "btn btn-default btn-xs disabled"} %>
<% dotdot_attr={"class": "btn btn-default btn-xs disabled"} %>
<link rel="stylesheet" href="//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">
<div class="row" id="extraTableInfo">
    <div class="col-lg-5 col-md-5 col-sm-2 col-xs-2">
        <span font-style: italic;>Click on a site to go to graphs</p>
    </div>
    <div class="col-md-4 col-sm-2 col-xs-2" id="tableDates">
        <form id="tableDateForm" action="">
            <div class="dateField">
                <p>Date: <input type="text" id="datepicker" name="date" placeholder="${date_chosen}"></p>
                <input type="hidden" name="location" value="${location}"/>
            </div>
        </form>
    </div>
</div>
<div class="row" id="tableContainer">
<table>
            <tr>
                      <th class="domainTableHeader">Site</th>
                      <th class="rankTableHeader">Rank</th>
                      <th class="weekTableHeader">Last Week</th>
                      <th class="fullTableHeader">Full Url</th>

            </tr>
            <% hasEntry = False %>
            <% passed_front_page = False %>
            % for line in table_entries:
                 <% hasEntry = True %>
                 <tr ${'class=tenLine' if not line.front_page and not passed_front_page else ''}>
                      <td ${'class=topTenDomain' if line.front_page else 'class=tableDomain'}>
                      <a href="/results/${tablename}/${line.domain}?location=${location}">${line.domain}
                      </a></td>
                      <td style="width:15px;overflow: hidden;" class="tablePosition">${line.position}</td>
                      <td>
                      % if line.week_position:
                          <span ${'style=display:inline-block;' if (line.position - line.week_position) < -4 else ''} class="upMyArrow">&#x21D1;</span>
                          <span ${'style=display:inline-block;' if (line.position - line.week_position) > 4 else ''} class="downMyArrow">&#x21D3;</span>
                          <span ${'style=display:inline-block;' if (line.position - line.week_position)==0 else ''} class="centreMyArrow">&#x21D4;</span>
                          <span ${'style=display:inline-block;' if -4 <= (line.position - line.week_position) < 0 else ''} class="supMyArrow">&#x21d7;</span>
                          <span ${'style=display:inline-block;' if 0 < (line.position - line.week_position) <= 4 else ''} class="sdownMyArrow">&#x21d8;</span>
                      % endif
                      <span>${line.week_position}</span>
                      </td>
                 <td class="fullUrlEntry"><a href="${line.full_url.decode('utf8')}" target="_blank">${line.full_url.decode('utf8')}</a></td>
                 </tr>
                 % if not line.front_page:
                    <% passed_front_page = True %>
                 % endif
            % endfor
            % if not hasEntry:
                <span style="color:red;">Oh...It seems there are no results for this date. :(</span>
            % endif
 </table>
 </div>

<script>
$(function() {
$( "#datepicker" ).datepicker({
  changeMonth: true,
  changeYear: true,
  dateFormat: "yy-mm-dd",
  onSelect : function(){
        $('#tableDateForm').submit();
        }
});
});
</script>
