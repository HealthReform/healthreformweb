var name = ""
var pass = ""
var id = ""
var email = ""

var main = function(){
           
            edit();
            cancel();
    
            
        };

 function edit(){
     
     $("#name").attr("disabled","disabled");
     $("#hospid").attr("disabled","disabled");
     $("#hospass").attr("disabled","disabled");
     $("#email").attr("disabled","disabled");
     
     
      $(".container").on("click","#edit",function(){
            $("#name").removeAttr("disabled","disabled");
            $("#hospid").removeAttr("disabled","disabled");
            $("#hospass").removeAttr("disabled","disabled");
            $("#email").removeAttr("disabled","disabled");
            
          
            $(this).remove();
            
            name = $("#name").attr("placeholder");
            id = $("#hospid").attr("placeholder");
            pass =$("#hospass").attr("placeholder");
            email = $("#email").attr("placeholder");
          
            $("#name").attr("value",name);
            $("#hospid").attr("value",id);
            $("#hospass").attr("value",pass);
            $("#email").attr("value",email);
          
            var cancel = $('<input type = "button" id ="cancelEdit" class="btn btn-default" value = "Cancel edit"/>');
            var change = $('<button type="submit" class="btn btn-default" id = "change" name = "action" value = "change" >Submit Changes</button>');
            
            $(".button").append(cancel);
            $(".button").append(change);
          
            
            
            
               
           });
     
       
     
     
 }
function cancel(){
    
     $(".container").on("click","#cancelEdit",function(){
         
             
            $("#name").attr("disabled","disabled");
            $("#hospid").attr("disabled","disabled");
            $("#hospass").attr("disabled","disabled");
            $("#email").attr("disabled","disabled");
         
            $("#name").attr("placeholder",name);
            $("#hospid").attr("placeholder",id);
            $("#hospass").attr("placeholder",pass);
            $("#email").attr("placeholder",email);
          
            $(this).remove();
            $("#change").remove();
          
            var edit = $('<button type="button" class="btn btn-default" id = "edit" >Edit Settings</button>');
            $(".button").append(edit);
            
            
               
           });
    
    

    
}
     
$(document).ready(main);   
     