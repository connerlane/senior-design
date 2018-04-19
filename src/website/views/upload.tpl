% rebase("layout.tpl", title="Upload")
% if "permissions" in sess and sess["permissions"] == "MANAGER":
<head>
    <!--Import Google Icon Font-->
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <!--Import materialize.css-->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-beta/css/materialize.min.css">


    <!--Let browser know website is optimized for mobile-->
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    
  </head>
    <header class="header">
      <div class="container">
        <div class="row" style="text-align: center;border-radius: 12px; margin-top: 15%">
          <div class="col s12">
            <h3 class="black-text lighten-1">Upload Training Data</h3>
            <hr width="75%" align="center">
          </div>
        </div>
      </div>
    </header>
    <body class = "container">   
      <div class = "row" style="text-align: center; margin-top: 10%">
         <form class = "col s4 offset-s4">
            <div class = "row">
               <label>Please choose a file to upload.</label>
               <div class = "file-field input-field">
                  <div class = "btn waves-effect waves-light btn-large blue darken-4 z-depth-5">
                     <span>Browse</span>
                     <input type = "file" />
                  </div>
                  
                  <div class = "file-path-wrapper">
                     <input class = "file-path validate" type = "text"
                        placeholder = "Upload file" />
                  </div>
               </div>
            </div>
         </form>       
      </div>
   </body>
   <footer class="page-footer white" style="margin-top: 19%">
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