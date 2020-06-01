function signup(event){
event.preventDefault();

$(document).ready(function(){

    $.ajax({
        data:{
            name:$("#name").val(),
            email:$("#email").val(),
            password:$("#password").val(),
        },
        type:"POST",
        url:" http://127.0.0.1:5000/signup"
    })
    .done(function(data){
        $("#output").text(data.output).show();
    })
})

}