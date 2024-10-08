function renderAnnouncements(data) {
    // Empty old data
    $("#announcements").empty()

    // Insert all of the new data
    $.each(data, function(i, datum){
        renderAnnouncement(datum["subject"], datum["body"])
    })
}

function renderAnnouncement(subjectText, bodyText) {
    var announcement = $("<div class='announcement'>")
    var subject = $("<span class='announcement-subject'>")
    var body = $("<span class='announcement-body'>")

    $(subject).html(subjectText)
    $(body).html(bodyText)

    $(announcement).append(subject)
    $(announcement).append(body)
    $("#announcements").append(announcement)

    // Clear text inputs
    $("#new-announcement-subject").val("")
    $("#new-announcement-body").val("")
}

function saveAnnouncement(subjectText, bodyText) {
    var dataToSave = {
        "subject": subjectText,
        "body": bodyText
    }

    $.ajax({
        type: "POST",
        url: "post_announcement",
        dataType : "json",
        contentType: "application/json; charset=utf-8",
        data : JSON.stringify(dataToSave),
        success: function(result) {
            var allData = result["data"]
            data = allData
            renderAnnouncements(data)
        },
        error: function(request, status, error) {
            console.log("Error");
            console.log(request)
            console.log(status)
            console.log(error)
        }
    });
}

$(document).ready(function(){
    // When the page loads, render all of the announcements
    renderAnnouncements(data)

    $("#submit-button").click(function(){
        var subject = $("#new-announcement-subject").val()
        var body = $("#new-announcement-body").val()

        saveAnnouncement(subject, body);
    })
})