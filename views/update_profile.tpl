% rebase("layout.tpl", title="Update Profile")
% if "permissions" in sess and sess["permissions"] == "MANAGER":
<div class="container">
  <div class="row">
    <div class="twelve columns" style="margin-top: 4%;  ">
      <h2 style="text-align: center">Update Profile</h2>
    </div>
  </div>
  % if defined('success'):
  <div class="row" style="margin-left: 35%">
    % if success:
    <h5 style="color: green">Success! Profile updated.</h5>
    % else:
    <h5 style="color: red">Something Went Wrong. Try again.</h5>
    % end
  </div>
  % end
  <hr>

  <div class = "row">
    <div class="four columns">
      <h5 style="text-align: center"></h5>
    </div>
    <div class="four columns">
      <h5 style="text-align: center">Change Password</h5>
    </div>
  </div>
  <form action="/change_password" method="POST" style="margin-left: 35%">
    <fieldset>
      <div class="row" style="margin-top: 5%">
        <div class="six columns">
          <label for="current_password">Current Password</label>
          <input class="u-full-width" id="current_password" type="password"  name="current_password">
        </div>
      </div>
      <div class="row">
        <div class="six columns">
          <label for="new_password">New Password</label>
          <input class="u-full-width" id="new_password" type="password"  name="new_password">
        </div>
      </div>
      <a class="button" href="/">Cancel</a>
      <input class="button-primary" style="margin: 3%" type="submit" value="Update Password">
    </fieldset>
  </form>
</div>
% else:
% include('login.tpl')