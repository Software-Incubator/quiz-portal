function JSalert(){
    swal({
            title: "Are you sure you want to exit?",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "Yes",
            cancelButtonText: "Cancel",
            closeOnConfirm: false,
            closeOnCancel: false
        },
        function(isConfirm){
        if (isConfirm)    {
            window.location.href = session_out;
        }
        else {
            swal.close();
        }
    });
}