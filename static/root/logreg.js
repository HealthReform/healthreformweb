  var main = function(){
           
            $(".container").hide().fadeIn(1000);
            
            moduleFocus();
            signDescriptions();
            loginEnable();
            
        };
            
        function loginEnable(){
            
            $(".navbar-btn").addClass("Disabled");
            
           $("#username").on("keyup",function(){
               var username =  $("#username").val();
               var password = $("#password").val();
               if(username!=''&& password!=''){
                   $(".navbar-btn").removeClass("Disabled");
               }
               else{
                   $(".navbar-btn").addClass("Disabled");
               }
               
           });
            
           $("#password").on("keyup",function(){
               var username =  $("#username").val();
               var password = $("#password").val();
               if(username!=''&& password!=''){
                   $(".navbar-btn").removeClass("Disabled");
               }
               else{
                 $(".navbar-btn").addClass("Disabled");  
               }
               
           });
           
            
           
            
        }
        function checkFields(){
            
            var hospName = $("#hospName").val();
            var hospID = $("#hospID").val();
            var hospPas = $("#hospPas").val();
            var repassword = $("#repassword").val();
            if(hospName!= '' && hospID != '' && hospPas != '' && repassword!='' && repassword==hospPas){
                $(".sign").removeClass("disabled");   
            }
            else{
                $(".sign").addClass("disabled");
            }
            
        }
            
        function signDescriptions(){
            $("#hospName").on("focusin",function(){
                
                var warning = $("<p>").text("Please enter full hospital name").addClass("alert alert-info");
                $(this).closest(".form-group").append(warning);
                $(this).closest('.form-group').children(".alert").fadeOut(2000);
                
                
            });
            
            $("#hospID").on("focusin",function(){
                
                var warning = $("<p>").text("Please enter hospital ID").addClass("alert alert-info");
                $(this).closest(".form-group").append(warning);
                $(this).closest('.form-group').children(".alert").fadeOut(2000)
                
            });
        
            
            $("#hospPas").on("focusin",function(){
                
                var warning = $("<p>").text("Please enter at least 8 word password(one capital,one lowercase,one number)").addClass("alert alert-info");
                $(this).closest(".form-group").append(warning);
                $(this).closest('.form-group').children(".alert").fadeOut(2000)
                
            });
          
            
            $("#repassword").on("focusin",function(){
                
                var warning = $("<p>").text("Please enter same password again").addClass("alert alert-info");
                var passWarn = $("<p>").text("Passwords Do Not Match").addClass("alert alert-info")
                $(this).closest(".form-group").append(warning);
                $(this).closest('.form-group').children(".alert").fadeOut(2000)
                
                
            });
            
              $("#repassword").on("keyup",function(){
                
                
                var passWarn = $("<p>").text("Passwords Do Not Match").addClass("alert alert-danger")
                var hospPas = $("#hospPas").val();
                var repassword = $("#repassword").val();
                if(hospPas != repassword){
                    $(this).closest('.form-group').children(".alert").remove()
                    $(this).closest(".form-group").append(passWarn);
                    $(this).closest('.form-group').children(".alert").fadeOut(2000)
                }
                else{
                     $(this).closest('.form-group').children(".alert").remove();
                }
                
                
                
            });
            
              $(".signup").on("focusout",function(){
                
                $(this).closest('.form-group').children(".alert").remove();
               
               
                
                
            });
             $(".signup").on("keyup",function(){
                
                
               checkFields();
               
                
                
            });
            
            
            $(".sign").addClass("disabled");
            
            
            
        }
            
        function moduleFocus(){
            
             $(".col-md-6").on("mouseenter",function(){
                $(this).css({"color":"black","border":"2px solid"});
                
            });
            $(".col-md-6").on("mouseleave",function(){
                $(this).css({"color":"white","border":"none"});
                
                
            });
            
        }
            
        $(document).ready(main);