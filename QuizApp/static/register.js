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

    // Check if the passwords match
    if (password !== repeatPassword) {
        alert('Passwords do not match');
        return;
    }

    // Create a new user object
    const userData = {
        name,
        email,
        password
    };

    
    $.ajax({
        type: 'POST',
        url: '/register-user',
        data: JSON.stringify(userData),
        contentType: 'application/json',
        success: function (data) {
            alert('User created successfully!');
            window.location.href = '/';
        },
        error: function (xhr, status, error) {
            alert('Error creating user');
        }
    });
});