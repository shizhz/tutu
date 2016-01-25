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
        var msg_box = $('#message-input')[0];

        Mousetrap(msg_box).bind('enter', function(e) {
            var suggestion_menu_visible = $('div.tt-menu').is(":visible");
            if(suggestion_menu_visible) {
                console.log("menu is visible, ignore logic here");
                return false;
            }
            console.log('# TODO: submit the command');
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
        initHotkeyBindings();
        initTypeahead();
        initFocus();
    });

    // API
    return {};
})();
