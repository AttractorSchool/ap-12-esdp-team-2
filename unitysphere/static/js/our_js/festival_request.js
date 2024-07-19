function ApproveFestivalRequest(btn) {
    let csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value
    let requestID = btn.getAttribute('request-id')
    $.ajax({
        type: "post",
        url: `/api/v1/festival/join_requests/${requestID}/request_action/`,
        data: {
            "action": "approve",
        },
        headers: {
            'Authorization': 'Token ' + localStorage.getItem('apiToken'),
            "X-CSRFToken": csrfToken
        },
        success: function (response) {
            console.log(response)
            let requestStatusStr = document.getElementById(`request-status-${requestID}`)
            requestStatusStr.innerText = 'Принят'
            requestStatusStr.className = 'request_status d-block font-weight-bold';
            requestStatusStr.classList.add('text-success')
        },
        error: function (response) {
            console.log(response)
        },
    });
}

function RejectFestivalRequest(btn) {
    let csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value
    let requestID = btn.getAttribute('request-id')
    $.ajax({
        type: "post",
        url: `/api/v1/festival/join_requests/${requestID}/request_action/`,
        data: {
            "action": "reject",
        },
        headers: {
            'Authorization': 'Token ' + localStorage.getItem('apiToken'),
            "X-CSRFToken": csrfToken
        },
        success: function (response) {
            console.log(response)
            let requestStatusStr = document.getElementById(`request-status-${requestID}`)
            requestStatusStr.innerText = 'Отклонен'
            requestStatusStr.className = 'request_status d-block font-weight-bold';
            requestStatusStr.classList.add('text-danger')
        },
        error: function (response) {
            console.log(response)
        },
    });
}