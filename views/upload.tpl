% rebase("layout.tpl", title="Upload") 
% if "permissions" in sess and sess["permissions"] == "MANAGER":

<head>
  <!--Import Google Icon Font-->
  <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
  <!--Import materialize.css-->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-beta/css/materialize.min.css">


  <!--Let browser know website is optimized for mobile-->
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Personality Prediction 3.0</title>
</head>
<div class="section white">
  <div class="row" style="float: left; text-align: center; margin-top: 4%; margin-bottom: 5%">
    <a class="waves-effect waves-light white-text btn-small blue darken-4 z-depth-5" style="border-radius: 12px" href="/">
      <i class="material-icons right">arrow_back</i>Back to Home</a>
  </div>
</div>
<header class="header">
  <div class="container">
    <div class="row" style="text-align: center;border-radius: 12px; margin-top: 2%; margin-bottom: 5%">
      <div class="col s12">
        <h4 class="black-text lighten-1">Upload</h3>
      </div>
    </div>
  </div>
</header>

<body class="container">
  <div class="section white">
    <div class="row" style="text-align: center; margin-top: 3%; margin-bottom: 0%">
      <div class="col s6">
        <a class="waves-effect waves-light white-text btn-large blue darken-4 z-depth-5" style="border-radius: 12px; padding-top: 15px;height: 90px; width: 400px"
        href="/upload_train_page">
          Upload Juji .csv</a>
      </div>
      <div class="col s6">
        <a class="waves-effect waves-light white-text btn-large blue darken-4 z-depth-5" style="border-radius: 12px; padding-top: 15px; height: 90px; width: 400px"
        href="/upload_model">
          Upload Model State</a>
      </div>
    </div>
  </div>
</body>
<!--JavaScript at end of body for optimized loading-->
<script type="text/javascript" src="https://code.jquery.com/jquery-2.1.1.min.js">
</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-beta/js/materialize.min.js"></script>
<script> 
  $(document).ready(function () {
    $('input.autocomplete').autocomplete({
      data: {
        "Apple": null,
        "Microsoft": null,
        "Google": 'https://placehold.it/250x250'
      },
    });
  });
</script>
</body>

</html>

% else: 
% include('login.tpl')