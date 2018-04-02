% rebase("layout.tpl", title="Store App - Update")
% if "permissions" in sess and sess["permissions"] == "MANAGER":
<div class="container">
  <div class="row">
    <div class="twelve column" style="margin-top: 10%">
      <h4 style="text-align: center">{{question}}</h4>
    </div>
  </div>
  <form action="/question" method="POST">
    <fieldset>
      <div class="row" style="margin-top: 5%">
        <textarea class="u-full-width" style="height: 200px" placeholder="Enter text..." id="answer" name="answer"></textarea>
      </div>
      <!-- <input type="text" x-webkit-speech> -->
      <a class="button" href="/" style="margin: 3%; margin-left: 0%">Cancel</a>
      <input class="button-primary" type="submit" value="Next">
    </fieldset>
  </form>
</div>
% else:
% include('denied.tpl')
