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

    
    {{!base}}
    
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
