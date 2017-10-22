<%inherit file="layout.mako"/>

<%def name="title()">
    Guess the hero: DAC edition
</%def>

<%def name="meta_keywords()">
    Guess hero, DAC, dota
</%def>

<%def name="meta_description()">
    Guess the hero: DAC edition
</%def>

<link rel="stylesheet" href="/static/awesomplete/awesomplete.css" />
<script src="/static/awesomplete/awesomplete.min.js" async></script>

<div class="row">
    <h2>Items</h2>
            <div class="card">
        <div class="card-content">
            <p>
            Current streak: ${user.streak}
            </p>
            <p>
            Max streak: ${user.max_streak}
            </p>
            <p id="${'positiveMessage' if success else 'negativeMessage'}">
            ${message}
            </p>
            % if success != True:
            <p>
                Correct hero was <a href="https://www.stratz.com/match/${match_id}" target="_blank">${correct_hero}</a>
            </p>
            % endif
        </div>
            </div>
    <div class="col s6">
        <div class="card">
        <div class="card-content">
            % for item in items:
                <img src="/static/images/items/${item}.png"/>
            % endfor
        </div>
        </div>
        <h3>Guess&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span id="timer">30 seconds</span></h3>
        <div class="card" id="guessSection" style="display: block;">
        <div class="card-content">
        <form action="/doGuess">
            Leaderboard name: <input type="text" name="username" value="${user.username if user.username else ''}"/>
            Guess: <input type="text" name="guess" list="heroes" class="awesomplete"/>
            <datalist id="heroes">
                % for h in heroes:
                    <option>${h["name"]}</option>
                % endfor
            </datalist>

            <button type="submit" class="btn waves-effect waves-light">Enter</button>
        </form>
        </div>
        </div>

        <div class="card" id="reloadSection" style="display: none;">
        <div class="card-content">
        <form action="/doGuess">
            <input type="hidden" name="username" value="${user.username}"/>
            <input type="hidden" name="guess" value=""/>
            <button type="submit" class="btn waves-effect waves-light">Reload</button>
        </form>
        </div>
        </div>
    </div>

<div class="col s6">
    <h3>Leaderboard</h3>
    <div class="card-content">
    <p>Congratulations to Thekmart for finishing top of Kiev hero guesser with 9!</p>
    </div>
    <table id="leaderboardTable" class="card-table striped">
        <tr>
            <th class="guessPositionHeader">Position</th>
            <th class="playerHeader">Player</th>
            <th class="streakHeader">Streak</th>
        </tr>
        % for i, player in enumerate(players):
            <tr>
                <td>${i+1}</td>
                <td>${player.username if player.username else "Anon"}</td>
                <td>${player.max_streak}</td>
            </tr>
        % endfor
    </table>
</div>


    <script>
// Set the date we're counting down to
var seconds = 45
var countDownDate = new Date().getTime() + 30000;

// Update the count down every 1 second
var x = setInterval(function() {
    var now = new Date().getTime();
    var distance = countDownDate - now;

    var seconds = Math.floor((distance % (1000 * 60)) / 1000);

    document.getElementById("timer").innerHTML = seconds + " seconds";

    // If the count down is over, write some text
    if (distance < 0) {
        clearInterval(x);
        document.getElementById("timer").innerHTML = "Out of time!";
        document.getElementById("guessSection").style.display = "none";
        document.getElementById("reloadSection").style.display = "block";
    }
}, 100);
</script>
