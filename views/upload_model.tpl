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
  <div class= "section white">
        <div class="row" style="float: left; text-align: center; margin-top: 4%; margin-bottom: 5%">  
            <a class="waves-effect waves-light white-text btn-small blue darken-4 z-depth-5" style="border-radius: 12px" href="/"><i class="material-icons right">arrow_back</i>Back to Home</a>
        </div>
    </div>

    <header class="header">
      <div class="container">
        <div class="row" style="text-align: center;border-radius: 12px">
          <div class="col s12">
            <h4 class="black-text lighten-1">Upload Model</h3>
              <body style="color: red; font-size: 20px">WARNING: this action will overwrite the state of the predictive model. You may want to <a href="/download/weight_matrix/model.npz">download the current model</a> as a backup before performing this action.</a></body>
          </div>
        </div>
      </div>
    </header>
    <body class = "container">   
      <div class = "row" style="text-align: center; margin-top: 3%">
         <form class = "col s4 offset-s4" action="/upload_model" method="post" enctype="multipart/form-data">
            <div class = "row">
               <label>Upload your .npz file here</label>
               <div class = "file-field input-field">
                  <div class = "btn waves-effect waves-light btn-large blue darken-4 z-depth-5">
                      <span>Browse</span>
                      <input type = "file" name="filename"/>
                   </div>
                  <div class = "file-path-wrapper">
                     <input class = "file-path" type = "text"
                        placeholder = "Upload file" />
                  </div>
               </div>
            </div>    
            <input type="submit" value="Start upload" />  
      </div>
   </body>
   <footer class="page-footer white" style="margin-top: 15%">
      <div class="footer-copyright blue darken-4">
        <div class="container">
          &#00169 2018 Copyright
        </div>
      </div>
    </footer>         <!--JavaScript at end of body for optimized loading-->
      <script type="text/javascript" src="https://code.jquery.com/jquery-2.1.1.min.js">
      </script>
      <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-beta/js/materialize.min.js"></script>
    </body>
  </html>
% else:
% include('login.tpl')