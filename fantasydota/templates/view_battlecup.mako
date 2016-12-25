<%inherit file="layout.mako"/>

<%def name="title()">
    Battlecup
</%def>

<%def name="meta_keywords()">
    Battlecup, Dota, fantasy, points, game
</%def>

<%def name="meta_description()">
    Battlecup page for fantasy dota game.
</%def>

<script type="text/javascript" src="/static/jquery.bracket.min.js"></script>
<link rel="stylesheet" type="text/css" href="/static/jquery.bracket.min.css" />

<div id="battlecupBlock" class="col-md-9">
    <p id="message">${"You are not signed up to play in a battlecup. Must have a valid account by the start of the days games" if not is_playing else ""}</p>
    <p>
    For ties, highest overall Boston Major fantasy points will be declared winner (0.1 points added to score)
    </p>
    <div class="bcupSeries col-md-3" style="width: 230px; margin-right: 40px">
        <a href="https://www.dotabuff.com/esports/series/166404" target="_blank">Semi final 1</a>
    </div>
    <div class="bcupSeries col-md-3" style="width: 230px; margin-right: 40px">
        <a href="https://www.dotabuff.com/esports/series/166405" target="_blank">Semi final 2</a>
    </div>
    <div class="bcupSeries col-md-3" style="width: 230px; margin-right: 40px">
        <a href="https://www.dotabuff.com/esports/series/166406" target="_blank">Grand final</a>
    </div>
    <div id="battlecupBracket">
    </div>
</div>

% if not transfer_open:
    <div id="tableContainer" class="col-md-3">
        <table class="sortable" id="heroTable">
            <tr>
                <th class="teamHeader"><h4>Teams</h4></th>
            </tr>
        </table>
    </div>
% endif

<script>
    var singleElimination;

    // example of data
    var singleElimination1= {
  "teams": [              // Matchups
    ["Team 1", "Team 2"], // First match
    ["Team 3", "Team 4"]  // Second match
  ],
  "results": [            // List of brackets (single elimination, so only one bracket)
    [                     // List of rounds in bracket
      [                   // First round in this bracket
        [1, 2],           // Team 1 vs Team 2
        [3, 4]            // Team 3 vs Team 4
      ],
      [                   // Second (final) round in single elimination bracket
        [5, 6],           // Match for first place
        [7, 8]            // Match for 3rd place
      ]
    ]
  ]
};
console.log(singleElimination1);
    $.ajax({
            url: "/battlecupJson?battlecup_id=${battlecup_id}",
            type: "GET",
            //contentType: 'application/json',
            success: function(data){
                singleElimination = data["bracket_dict"];
                var hero_imgs = data["hero_imgs"];
                console.log(singleElimination);
                $('#battlecupBracket').bracket({
                    init: singleElimination,
                    teamWidth: 200,
                    matchMargin: 100});
                hero_imgs.forEach(function(element, index){
                    var name = element["pname"],
                    h_imgs = element["heroes"];
                    console.log(index);
                    console.log(h_imgs);
                    if (name != null){
                        var newRow = "<tr class='" + name + "PRow'><td class='playerName'>" + name + "</td><td></td><td></td><td></td></tr>"
                            + "<tr class='listHeroes'>";
                        if (h_imgs.length > 0){
                        for (j=0; j < h_imgs.length; j++){
                            newRow+= "<td class='teamHeroIcon'><img class='heroIcon' src='/static/images/" + h_imgs[j].replace(" ", "_") + "_icon.png' \></td>";
                        }}
                        newRow += "</tr>";
                        $("#heroTable").append(newRow);
                    }
                    $(".blabel").filter(function(index) { return $(this).text() === name; }).hover(function(){
                        var pRow = $("#heroTable").find("." +name + "PRow");
                        pRow.addClass('highlight');
                        pRow.next().addClass('highlight');
                    },
                        function(){
                            var pRow = $("#heroTable").find("." +name + "PRow");
                            pRow.removeClass("highlight");
                            pRow.next().removeClass('highlight');
                        }
                    );
                })
                }
            });
    </script>