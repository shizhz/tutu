var Tutu = Tutu || (function() {
    function removeSuggestionMenu() {
        var cmdSegs = $('#mesage-input').val().split();
        var suggestions = $('div.tt-menu div.tt-suggestion>strong');
        if(suggestions.length == 1) {
            var lastCmdSeg = cmdSegs[cmdSegs.length - 1];
            var suggestion = lastCmdSeg == suggestions.text();
            // TODO: select it
        }
    }

    function initHotkeyBindings() {
        var msg_box = $('#message-input')[0];

        Mousetrap(msg_box).bind('enter', function(e) {
            var suggestion_menu_visible = $('div.tt-menu').is(":visible");
            removeSuggestionMenu();
            if (suggestion_menu_visible) {
                console.log("menu is visible, ignore logic here");
                return false;
            }
            console.log('# TODO: submit the command');
        });
    }

    function initTypeahead() {
        var commands = new Bloodhound({
            datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
            queryTokenizer: Bloodhound.tokenizers.whitespace,
            prefetch: '/api/commands'
        });

        $('.typeahead').typeahead({
                hint: true,
                highlight: true,
                minLength: 1,
                menuConfig: {
                    position: 'top'
                }
            }, {
                name: 'commands',
                display: 'name',
                source: commands,
                templates: {
                    header: '<h3 class="suggestion-menu">Commands</h3>'
                }
            }
        );
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
