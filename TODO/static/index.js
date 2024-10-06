$(document).ready(function () {
    $("#addForm").hide();
    $("#updateForm").hide();

    // Check if the token is stored in local storage
    const token = localStorage.getItem('token');
    console.log("Retrieved Token:", token);  // Debugging line

    // Show the add form
    $("#showAddForm").click(function (e) {
        e.preventDefault();
        $("#addForm").slideToggle();
    });

    // Clear the add form
    $("#clearForm").click(function (e) {
        e.preventDefault();
        $("#title").val("");
        $("#description").val("");
        $("#addForm").slideUp();
    });

    // Handle form submission for adding new todo
    $("#addForm").submit(function (e) {
        e.preventDefault();
        const title = $("#title").val();
        const description = $("#description").val();

        if (title === "" || description === "") {
            alert("Please fill out both fields.");
            return;
        }

        $.ajax({
            url: '/todos',
            type: 'POST',
            contentType: 'application/json',
            headers: { 'Authorization': 'Bearer ' + token }, 
            data: JSON.stringify({ todoTitle: title, todoDescription: description }),
            success: function (response) {
                alert("Todo added successfully!");
                location.reload();
            },
            error: function (xhr, status, error) {
                alert("An error occurred: " + error);
                console.error("Error Details:", xhr.responseText);
            }
        });
    });

    // Handle delete button click
    $(document).on('click', '.deleteBtn', function (e) {
        e.preventDefault();
        const todoId = $(this).data('id');
        $.ajax({
            url: `/todos/${todoId}`,
            type: 'DELETE',
            contentType: 'application/json',
            headers: { 'Authorization': 'Bearer ' + token },  // Add token to headers
            success: function (response) {
                alert("Todo deleted successfully!");
                location.reload();
            },
            error: function (xhr, status, error) {
                alert("An error occurred: " + error);
                console.error("Error Details:", xhr.responseText);
            }
        });
    });

    // Handle update button click
    $(document).on('click', '.updateBtn', function (e) {
        e.preventDefault();
        const todoId = $(this).data('id');
        const title = $(this).data('title');
        const description = $(this).data('description');

        $("#update_todo_id").val(todoId);
        $("#update_title").val(title);
        $("#update_description").val(description);
        $("#updateForm").slideDown();
    });

    // Handle update form submission
    $("#updateTodoForm").submit(function (e) {
        e.preventDefault();
        const todoId = $("#update_todo_id").val();
        const title = $("#update_title").val();
        const description = $("#update_description").val();

        $.ajax({
            url: `/todos/${todoId}`,
            type: 'PUT',
            contentType: 'application/json',
            headers: { 'Authorization': 'Bearer ' + token },  // Add token to headers
            data: JSON.stringify({ todoTitle: title, todoDescription: description }),
            success: function (response) {
                alert("Todo updated successfully!");
                location.reload();
            },
            error: function (xhr, status, error) {
                alert("An error occurred: " + error);
                console.error("Error Details:", xhr.responseText);
            }
        });
    });

    // Handle clear update form
    $("#clearUpdateForm").click(function (e) {
        e.preventDefault();
        $("#updateForm").slideUp();
    });
});
