$(document).ready(function() {
    $('#ask-form').on('submit', function(e) {
        e.preventDefault();

        const userText = $('#user-text').val();
        $.ajax({
            url: '/ask',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ user_text: userText }),
            success: function(response) {
                $('#reply').text(response.reply);
            },
            error: function() {
                alert('An error occurred while processing your request.');
            }
        });
    });
});