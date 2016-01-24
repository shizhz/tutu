var Tutu = Tutu || (function() {
    var substringMatcher = function(strs) {
        return function findMatches(q, cb) {
            var matches, substringRegex;

            // an array that will be populated with substring matches
            matches = [];

            // regex used to determine if a string contains the substring `q`
            substrRegex = new RegExp(q, 'i');

            // iterate through the pool of strings and for any string that
            // contains the substring `q`, add it to the `matches` array
            $.each(strs, function(i, str) {
                if (substrRegex.test(str)) {
                    matches.push(str);
                }
            });

            cb(matches);
        };
    };

    var states = ['help', 'sh', 'list', 'a-very-long-name-here-what-ganna-happen?'];

    function initHotkeyBindings() {
        var msg_box = $('message-input');
        var msg_form = $('#message-form')[0];
        Mousetrap.bindGlobal('?', function() {
            msg_box.val('hot key bound');
        });

        Mousetrap(msg_form).bind('/', function(e) {
            if (e.preventDefault) {
                e.preventDefault();
            } else {
                e.returnValue = false;
            }
            var cmd = msg_box.val();
            console.log(cmd);
        });
    }

    function initTypeahead() {
        $('.typeahead').typeahead({
            hint: true,
            highlight: true,
            minLength: 1,
            menuConfig: {
                position: 'top'
            }
        }, {
            name: 'commands',
            source: substringMatcher(states)
        });
    }

    function initFocus() {
        $('#message-input').focus();
    }

    $(function() {
        initTypeahead();
        initHotkeyBindings();
        initFocus();
    });

    // API
    return {};
})();
