let baseURL = "http://127.0.0.1:8000/api/v1/festivals"

let btn = $('#FestivalParticipationRequest')
    btn.click(function (e) {
    let club = $('#selectedClub').val();
    let festival = $('#festivalId').val();

    $.ajax({
        url: `${baseURL}/${festival}/festival_action/`,
        type: 'post',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({
            action: "join",
            club: club,
        }),
        success: function (response) {
            console.log(response)
            btn.attr( "disabled", true).html("Запрос отправлен").addClass("btn-light")
        },
        error: function(response, status){
            console.log(response, status)
            btn.attr( "disabled", true).html("Ошибка в запросе").addClass("btn-light")
        }
    })
});