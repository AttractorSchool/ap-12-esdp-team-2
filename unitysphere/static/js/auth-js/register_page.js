let RegisterURL = "/api/v1/register";
let RegisterVerifyURL = "/api/v1/register/verify";


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
        url: RegisterURL,
        headers: {
            "X-CSRFToken": csrfToken,

        },
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
            localStorage.setItem("session_id", response.session_id)
            swapForm(response.phone)
        },
        error: function (response) {
            console.log(response)
            insertAllErrors(response.responseJSON)
        }
    });    
    
});

jQuery("#verify_user_form").submit(function (e) { 
    e.preventDefault();
    formData = new FormData(jQuery(this)[0]);
    let csrfToken = formData.get("csrfmiddlewaretoken");
    let code_input = $("#id_sms_code").val();
    let data = {
        "user_session_id": localStorage.getItem("session_id"),
        "sms_code": code_input
    }

    clearFieldErrors()
    jQuery.ajax({
        type: "post",
        url: RegisterVerifyURL,
        headers: {
            "X-CSRFToken": csrfToken
        },
        data: JSON.stringify(data),
        processData: false,
        contentType: "application/json;charset=utf-8",
        success: function (response) {
            console.log(response)
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

function swapForm(phoneNumber) {
    let verifyMessageElm = document.getElementById("verify-message")
    let formRegister = document.getElementById("register_user_form")
    let formVerify = document.getElementById("verify_user_form")
    formRegister.style.display = "none"
    formVerify.style.display = "block"
    let formTitle = document.getElementById("form-title")
    formTitle.innerText = "Введите код из СМС"
    verifyMessageElm.innerText = `Мы отправили его на номер: ${phoneNumber}`
}
