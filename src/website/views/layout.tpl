<!DOCTYPE html>
<html lang="en">
<head>

  <!-- Basic Page Needs
    –––––––––––––––––––––––––––––––––––––––––––––––––– -->
    <meta charset="utf-8">
    <title>{{title}}</title>
    <meta name="description" content="">
    <meta name="author" content="">

  <!-- Mobile Specific Metas
    –––––––––––––––––––––––––––––––––––––––––––––––––– -->
    <meta name="viewport" content="width=device-width, initial-scale=1">

  <!-- FONT
    –––––––––––––––––––––––––––––––––––––––––––––––––– -->
    <!-- <link href="//fonts.googleapis.com/css?family=Raleway:400,300,600" rel="stylesheet" type="text/css"> -->

  <!-- CSS
    –––––––––––––––––––––––––––––––––––––––––––––––––– -->
    <link rel="stylesheet" href="/static/css/normalize.css">
    <link rel="stylesheet" href="/static/css/skeleton.css">
    <!--<link rel="stylesheet" href="/static/css/materialize.css"> -->

  <!-- Favicon
    –––––––––––––––––––––––––––––––––––––––––––––––––– -->
 <!--    <link rel="icon" type="image/png" href="/static/images/favicon.png"> -->

</head>
<body>
    % if "username" in sess or title == "Login":
    % if "username" in sess:
    <div style="text-align: right; margin: 3% 3% -10%">
      <div class="row">
        <h5>
        % if 'has_picture' in sess and sess['has_picture']:
        <img src="/profile/{{ sess['username'] }}/image" alt="Profile Picture" style="max-width: 100%; max-height: 100%; width: 4vw; height: 4vw; margin-right: 1%">
        %else:
        <img src="/static/images/generic-profile.jpg" alt="Profile Picture" style="max-width: 100%; max-height: 100%; width: 4vw; height: 4vw; margin-right: 1%">
        % end
        <a href="/update_profile/self">{{sess["username"]}} 
          %if sess["permissions"] == "MANAGER":
          &#9733; <!-- add a star -->
          %end
        </a></h5>
      </div>
      <h6><a style="color: orange" href="/logout">Logout</a></h6>
    </div>
    % end
  <!-- Primary Page Layout
    –––––––––––––––––––––––––––––––––––––––––––––––––– -->
    {{!base}}

    %else:
    <div class="container">
      <div class="row">
        <div class="twelve column" style="margin-top: 15%">
          <h4 style="text-align: center">You are not logged in</h4>
          <a href="/login" style="text-align: center; margin-top: 10%"><h5>Click here to log in</h5></a>
        </div>
      </div>
    </div>
<script type="text/javascript" src="js/materialize.min.js"></script>
<script type="text/javascript" src="https://code.jquery.com/jquery-2.1.1.min.js">
      </script>
      <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-beta/js/materialize.min.js"></script>
      <script>
        $(document).ready(function(){
          $('.parallax').parallax();
        });
      </script>
<!-- End Document
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
</body>
</html>
