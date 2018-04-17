% rebase("layout.tpl", title="Survey")
% if "permissions" in sess and sess["permissions"] == "MANAGER":
<div class="container">
  <div class="row">
    <div class="twelve column" style="margin-top: 10%">
      <h6 style="text-align: center">Question {{index}} / 39</h6> 
      <h4 style="text-align: center">{{question}}</h4>
    </div>
  </div>
  <form action="/question" method="POST">
    <fieldset>
      <div class="row" style="margin-top: 5%">
        <textarea class="u-full-width" style="height: 200px" placeholder="Enter text..." id="answer" name="answer"></textarea>
      </div>
      <img onclick="startDictation()" src="//i.imgur.com/cHidSVu.gif" />
      <!-- <input type="text" x-webkit-speech> -->
      <a class="button" href="/" style="margin: 3%; margin-left: 0%">Cancel</a>
      <input class="button-primary" type="submit" value="Next">
    </fieldset>
  </form>
</div>
<script>
 function startDictation() {

   if (window.hasOwnProperty('webkitSpeechRecognition')) {

     var recognition = new webkitSpeechRecognition();

     recognition.continuous = false;
     recognition.interimResults = false;

     recognition.lang = "en-US";
     recognition.start();

     recognition.onresult = function(e) {
       document.getElementById('answer').value = e.results[0][0].answer;
       recognition.stop();
     };

     recognition.onerror = function(e) {
       recognition.stop();
     }

   }
 }
</script>
% else:
% include('denied.tpl')
