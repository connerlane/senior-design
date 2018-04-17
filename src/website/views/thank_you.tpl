% rebase("layout.tpl", title="Store App - Update")
% if "permissions" in sess and sess["permissions"] == "MANAGER":
<div class="container">
  <div class="row">
    <div class="twelve column" style="margin-top: 10%">
      <h4 style="text-align: center">Thank you for taking the survey</h4>
    <br>
      <h6 style="text-align: center">We really appreciate it!</h6> 
    </div>
  </div>
  <br><br>
    <div class="row" style="margin-top: 5%; text-align: center">
        <div class="twelve columns">
            <a class="button button-primary" href="/">Done</a>
        </div>
    </div>
</div>

% else:
% include('denied.tpl')
