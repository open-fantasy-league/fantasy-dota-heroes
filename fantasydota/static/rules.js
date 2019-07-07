var scoringRulesUl = $("#scoringRules");
var r = new Array(), j = -1;
getLeagueInfo(false, true, false, true).then(function() {
    for (const [key, value] of Object.entries(league.scoring)){
        r[++j] = '<li ';
        var statField = league.statFields.find(function(x){return x.name == key});
        if (statField){
            r[++j] = 'title="';
            r[++j] = statField.description;
            r[++j] = '"';
        }
        r[++j] = '>'
        r[++j] = key;
        r[++j] = ': '
        if (value.any){
            r[++j] = value.any;
        }
        else{
            r[++j] = '<ul>';
            for (const [key2, value2] of Object.entries(value)){
                r[++j] = '<li>';
                r[++j] = key2;
                r[++j] = ': '
                r[++j] = value2;
                r[++j] = '</li>';
            }
            r[++j] = '</ul>';
        }
        r[++j] = '</li>';
        scoringRulesUl.html(r.join(''));
    }
})