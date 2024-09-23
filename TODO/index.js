$(document).ready(function () {


    $("#showAddForm").click(function (e) { 
        e.preventDefault();
        // console.log("herere")
        $("#addForm").slideDown();
    });

    $("#clearForm").click(function (e) { 
        e.preventDefault();
        $("#title").val("");
        $("#description").val("");
        $("#addForm").slideUp();

    });

    


    //initials
    $("#addForm").hide();
});