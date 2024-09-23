const form = $('form');
const nameInput = $('#form3Example1c');
const emailInput = $('#form3Example3c');
const passwordInput = $('#form3Example4c');
const repeatPasswordInput = $('#form3Example4cd');

$('.btn-primary').on('click', async (e) => {
    e.preventDefault();

    // Get the form data
    const name = nameInput.val();
    const email = emailInput.val();
    const password = passwordInput.val();
    const repeatPassword = repeatPasswordInput.val();

    // Validate the input data
    if (!name || !email || !password || !repeatPassword) {

        $("#loginResult").html("Please fill in all fields");
        $("#loginResult").removeClass(); // Remove all existing classes
        $("#loginResult").addClass("alert alert-warning");
        $("#loginResult").slideDown();
        setTimeout(function () {
            $("#loginResult").slideUp();
        }, 3000);

        return;
    }

    if (password.length < 8) {

        $("#loginResult").html("Password must be at least 8 characters");
        $("#loginResult").removeClass(); // Remove all existing classes
        $("#loginResult").addClass("alert alert-warning");
        $("#loginResult").slideDown();
        setTimeout(function () {
            $("#loginResult").slideUp();
        }, 3000);

        return;
    }

    if (password !== repeatPassword) {

        $("#loginResult").html("Passwords do not match");
        $("#loginResult").removeClass(); // Remove all existing classes
        $("#loginResult").addClass("alert alert-warning");
        $("#loginResult").slideDown();
        setTimeout(function () {
            $("#loginResult").slideUp();
        }, 3000);

        return;
    }

    if (!/^[^@]+@[^@]+\.[^@]+$/.test(email)) {

        $("#loginResult").html("Invalid email address");
        $("#loginResult").removeClass(); // Remove all existing classes
        $("#loginResult").addClass("alert alert-warning");
        $("#loginResult").slideDown();
        setTimeout(function () {
            $("#loginResult").slideUp();
        }, 3000);

        return;
    }

    // Create a new user object
    const userData = {
        name,
        email,
        password
    };

    // console.log(userData)

    $.ajax({
        type: 'POST',
        url: '/register',
        data: JSON.stringify(userData),
        contentType: 'application/json',
        success: function (data) {
            $("#loginResult").html("User Created!! Redirecting to login page in 3 seconds!!");
            $("#loginResult").removeClass(); // Remove all existing classes
            $("#loginResult").addClass("alert alert-success");
            $("#loginResult").slideDown();
            setTimeout(function () {
                $("#loginResult").slideUp();
                window.location.href = '/';
            }, 3000);
        },
        error: function (xhr, status, error) {
            if (xhr.status === 400) {
                $("#loginResult").html("Please fill in all fields or password must be at least 8 characters");
                $("#loginResult").removeClass(); // Remove all existing classes
                $("#loginResult").addClass("alert alert-danger");
                $("#loginResult").slideDown();
                setTimeout(function () {
                    $("#loginResult").slideUp();
                }, 3000);
            }
            else if (xhr.status === 409) {
                $("#loginResult").html("Email already exists");
                $("#loginResult").removeClass(); // Remove all existing classes
                $("#loginResult").addClass("alert alert-warning");
                $("#loginResult").slideDown();
                setTimeout(function () {
                    $("#loginResult").slideUp();
                }, 3000);
            }
            else {
                $("#loginResult").html("Something went wrong!!");
                $("#loginResult").removeClass(); // Remove all existing classes
                $("#loginResult").addClass("alert alert-dark");
                $("#loginResult").slideDown();
                setTimeout(function () {
                    $("#loginResult").slideUp();
                }, 3000);
            }
        }
    });
});

//default
$("#loginResult").hide();