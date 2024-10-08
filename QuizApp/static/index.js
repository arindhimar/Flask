const form = $('form');
const emailInput = $('#form3Example3');
const passwordInput = $('#form3Example4');


$('#loginBtn').on('click', async (e) => {
    e.preventDefault();

    // Get the form data
    const email = emailInput.val();
    const password = passwordInput.val();


    if (!email || !password ) {

        $("#loginResult").html("Please fill in all fields");
        $("#loginResult").removeClass(); // Remove all existing classes
        $("#loginResult").addClass("alert alert-warning");
        $("#loginResult").slideDown();
        setTimeout(function () {
            $("#loginResult").slideUp();
        }, 3000);

        return;
    }

    
    const userData = {
        email,
        password
    };

    
    $.ajax({
        type: 'POST',
        url: '/login-user',
        data: JSON.stringify(userData),
        contentType: 'application/json',
        success: function (data) {
            window.location.href = '/admin';
        },
        error: function (xhr, status, error) {
            if (error == "UNAUTHORIZED") {
                $("#loginResult").removeClass();
                $("#loginResult").html("Invalid Credentials!!");
                $("#loginResult").addClass("alert alert-danger");
                $("#loginResult").slideDown();
                setTimeout(function() {
                  $("#loginResult").slideUp();
                //   $("#loginResult").removeClass("alert alert-danger");
                }, 3000); 
            }
            else if(error == "NOT FOUND"){
                $("#loginResult").removeClass();
                $("#loginResult").html("New User??!!");
                $("#loginResult").addClass("alert alert-warning");
                $("#loginResult").slideDown();
                setTimeout(function() {
                  $("#loginResult").slideUp();
                //   $("#loginResult").removeClass("alert alert-danger");
                }, 3000); 
            }
            else{
                $("#loginResult").removeClass();
                $("#loginResult").html("Something went wrong!!");
                $("#loginResult").addClass("alert alert-dark");
                $("#loginResult").slideDown();
                setTimeout(function() {
                  $("#loginResult").slideUp();
                //   $("#loginResult").removeClass("alert alert-danger");
                }, 3000);
            }
            
        }
    });




    //default
    $("#loginResult").hide();
});