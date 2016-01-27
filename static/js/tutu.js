var Tutu = Tutu || (function() {
    function suggestion_menu_visible() {
        return $('div.tt-menu').is(":visible");
    }

    function removeSuggestionMenu(e) {
        if (suggestion_menu_visible()) {
            var suggestions = $('div.tt-menu div.tt-suggestion');
            var cmdSegs = $('#message-input').val().split();

            if(suggestions.length == 1) {
                var lastCmdSeg = $.trim(cmdSegs[cmdSegs.length - 1]);
                var suggestion = $.trim(suggestions.text());
                if (lastCmdSeg == suggestion) {
                    $('.typeahead').typeahead('val', suggestion);
                    $('.typeahead').typeahead('close');
                }
            }
        }
    }

    function initHotkeyBindings() {
        var msg_box = $('#message-input')[0];
        Mousetrap(msg_box).bind('enter', function(e) {
            removeSuggestionMenu();
            if (!suggestion_menu_visible()) {
                console.log("menu is visible, ignore logic here");
            }
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
