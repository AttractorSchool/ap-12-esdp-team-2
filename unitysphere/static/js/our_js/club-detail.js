function likeClub(btn) {
    let action_data = {
        'action': 'like'
    }
    let club_id = btn.getAttribute("club_id")
    $.ajax({
        type: "post",
        url: `http://127.0.0.1:8000/api/v1/clubs/${club_id}/club_action/`,
        data: action_data,
        headers: {'Authorization': 'Token ' + localStorage.getItem('apiToken')},
        success: function (response) {
            console.log(response)
        },
        error: function(response) {
            console.log(response)
        }
    });
}