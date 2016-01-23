var Tutu = Tutu || (function() {
    function init() {
        $('#message-input').focus();
        Mousetrap.bindGlobal('?', function() {
            $('#message-input').val('hot key bound');
        });
        Mousetrap($('#message-form')[0]).bind('tab', function(e) {
            if (e.preventDefault) {
                e.preventDefault();
            } else {
                e.returnValue = false;
            }
            var cmd = $('#message-input').val();
            console.log(cmd);
        });
    }

    $(function() {
        init();
    });

    // API
    return {
    };
})();
