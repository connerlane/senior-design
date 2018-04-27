% rebase("layout.tpl", title="Upload")
% if "permissions" in sess and sess["permissions"] == "MANAGER":
<head>
    <!--Import Google Icon Font-->
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <!--Import materialize.css-->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-beta/css/materialize.min.css">


    <!--Let browser know website is optimized for mobile-->
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Personality Prediction 3.0</title>
  </head>
    <div class= "section white">.
        <div class="row" style="float: left; text-align: center; margin-top: 4%; margin-bottom: 5%">  
            <a class="waves-effect waves-light white-text btn-small blue darken-4 z-depth-5" style="border-radius: 12px" href="/"><i class="material-icons right">arrow_back</i>Back to Home</a>
        </div>
    </div>
    <header class="header">
      <div class="container">
        <div class="row" style="text-align: center;border-radius: 12px; margin-top: 13%">
          <div class="col s12">
            <h3 class="black-text lighten-1">View/Download Data</h3>
            <hr width="75%" align="center">
          </div>
        </div>
      </div>
    </header>
    <body class = "container">   
      <div class="row">
        <div class="col s12">
          <div class="row">
            <div class="input-field col s12">
              <i class="material-icons prefix">search</i>
              <input type="text" id="autocomplete-input" class="autocomplete">
              <label for="autocomplete-input">Search By Name</label>
            </div>
          </div>
        </div>
      </div>
      <div class= "section white">.
          <div class="row" style="text-align: center; margin-top: 4%; margin-bottom: 5%">  
            <div class="col s4 offset-s4">
              <a class="waves-effect waves-light white-text btn-large blue darken-4 z-depth-5" style="border-radius: 12px; padding-top: 15px;height: 90px; width: 400px"><i class="material-icons right">arrow_downward</i>Download All Data</a>
            </div>
          </div>
        </div>
   </body>
   <footer class="page-footer white" style="margin-top: 2%">
      <div class="footer-copyright blue darken-4">
        <div class="container">
          &#00169 2018 Copyright
        </div>
      </div>
    </footer>         <!--JavaScript at end of body for optimized loading-->
      <script type="text/javascript" src="https://code.jquery.com/jquery-2.1.1.min.js">
      </script>
      <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-beta/js/materialize.min.js"></script>
      <script> 
        $(document).ready(function(){
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