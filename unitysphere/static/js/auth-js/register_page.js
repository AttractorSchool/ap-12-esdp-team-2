letRegisterURL = "/api/v1/register"


jQuery("#register_user_form").submit(function (e) { 
    e.preventDefault();
    formData = new FormData(jQuery(this)[0]);
    
    console.log(formData)
    let csrfToken = formData.get("csrfmiddlewaretoken");
    formData.delete("csrfmiddlewaretoken");
    
    clearFieldErrors()
    validatePasswords(formData)
    jQuery.ajax({
        type: "post",
        url: letRegisterURL,
        headers: {
            "X-CSRFToken": csrfToken,

        },
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
            localStorage.setItem("session_id", response.session_id)
        },
        error: function (response) {
            console.log(response)
            insertAllErrors(response.responseJSON)
        }
    });    
    
});


function validatePasswords(formData) {

    if (formData.get("password1") != formData.get("password2")) {
        blockErrors = document.getElementById(`errors_password2`)
        let errorElm = "<p class='text-danger text-center'>Пароли не совпадают</p>"
        blockErrors.innerHTML += errorElm
    } 

    let password = formData.get("password1")
    formData.delete("password1")
    formData.delete("password2")
    formData.append("password", password)
    
}


function insertAllErrors(errors) {
    for (let field_name in errors) {
        insertFieldErrors(field_name, errors[field_name])
    }
}


function insertFieldErrors(field_name, errors) {
    let blockErrors;
    if (field_name == "password") {
        blockErrors = document.getElementById(`errors_password2`)
    } else {
        blockErrors = document.getElementById(`errors_${field_name}`)
    }
    for (let i = 0; i < errors.length; i++) {
        let errorElm = `<p class="text-danger text-center">${errors[i]}</p>`;
        blockErrors.innerHTML += errorElm
    }
}

function clearFieldErrors() {
    let errorBlocks = document.getElementsByClassName("block-errors")
    for (let errorBlock of errorBlocks) {
        errorBlock.innerHTML = ""
    }
}