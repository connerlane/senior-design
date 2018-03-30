% rebase("layout.tpl", title="Personality Prediction 3.0")
  
    <head>
      <!--Import Google Icon Font-->
      <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
      <!--Import materialize.css-->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-beta/css/materialize.min.css">


      <!--Let browser know website is optimized for mobile-->
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
      <title>Personality Prediction 3.0</title>
    </head>

    <body>
      <main>
        <div class="parallax-container center valign-wrapper">
          <div class="row">
            <div class="col s12" style="margin-top: 15%; background: rgba(0, 0, 0, 0.7)">
              <h4 style="text-align: center; color:white">Personality Prediction 3.0</h4>
              <p style="text-align: center; font-weight: 200; color:white">Welcome to the app. Click a button to get started.</p>
            </div>
          </div>
          <div class="parallax">
            <img src="static/images/samford.jpeg">
          </div>
        </div>  
        <div class= "section white">.
          <div class="row" style="text-align: center; margin-top: 4%; margin-bottom: 5%">  
            <div class="col s4">
              <a class="waves-effect waves-light white-text btn-large blue darken-4 z-depth-5" style="border-radius: 12px; padding-top: 15px;height: 90px; width: 400px" href="/viewdownload"><i class="material-icons right">arrow_upward</i>Upload Data</a>
            </div>
            <div class="col s4">
              <a class="waves-effect waves-light white-text btn-large blue darken-4 z-depth-5" style="border-radius: 12px; padding-top: 15px; height: 90px; width: 400px" href="/upload"><i class="material-icons right">arrow_downward</i>View/Download Data</a>
            </div>
            <div class="col s4">
              <a class="waves-effect waves-light white-text btn-large blue darken-4 z-depth-5" style="border-radius: 12px; padding-top: 15px; height: 90px; width: 400px" href="/question"><i class="material-icons right">edit</i>Interview A Candidate</a>
            </div>
          </div>
          <hr width="75%" align="center">
        </div>

      </div>
    </main> 
      <footer class="page-footer white">
          <div class="container">
            <div class="row" style="text-align: center;">
              <div class="col s12">
                <h1 class="grey-text text-darken-2" style="font-size:45px">About Us</h2>
                <p class="grey-text text-darken-2" style="font-size: 15px">Personality Predicion 3.0 is a senior design project made to predict an interviewee's personality based off of their written words. Made by Conner Lane, Sara Locklar, Eric Agnitsch, and Jonathan McGuckin.</p>
              </div>
            </div>
          </div>
          <div class="footer-copyright blue darken-4">
            <div class="container">
              &#00169 2018 Copyright
            </div>
          </div>
        </footer>
      <!--JavaScript at end of body for optimized loading-->
      <script type="text/javascript" src="https://code.jquery.com/jquery-2.1.1.min.js">
      </script>
      <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-beta/js/materialize.min.js"></script>
      <script>
        $(document).ready(function(){
          $('.parallax').parallax();
        });
      </script>
    </body>
  %end
  
