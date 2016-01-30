var Tutu = Tutu || (function() {
    function suggestion_menu_visible() {
        return $('div.tt-menu').is(":visible");
    }

    function buildSuggestionCmd(rawInput, suggestion) {
        var cmdSegs = rawInput.split(/\W+/);
        return [].slice.call(cmdSegs, 0, -1).concat([suggestion]).join(' ');
    }

    function removeSuggestionMenu(e) {
        if (suggestion_menu_visible()) {
            var suggestions = $('div.tt-menu div.tt-suggestion');
            var rawInput = $('#message-input').val();
            var cmdSegs = rawInput.split(/\W+/);

            if(suggestions.length == 1) {
                var lastCmdSeg = $.trim(cmdSegs[cmdSegs.length - 1]);
                var suggestion = $.trim(suggestions.text());
                if (lastCmdSeg == suggestion) {
                    $('.typeahead').typeahead('val', buildSuggestionCmd(rawInput, suggestion));
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
        var initTabKeyed = function() {
            var rawInput;
            $('.typeahead').bind('typeahead:beforeselect typeahead:beforeautocomplete', function(e, suggestion) {
                rawInput = $('#message-input').val();
            });

            $('.typeahead').bind('typeahead:select typeahead:autocomplete', function(e, suggestion) {
                $('.typeahead').typeahead('val', buildSuggestionCmd(rawInput, suggestion.name));
            });
        };

        var commands = new Bloodhound({
            datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
            queryTokenizer: function(str) {
                if (str.endsWith(' ')) {
                    // don't show menu when enter whitespace
                    return ['_impossible_token_'];
                }
                // Only return the last word as query token
                return [].slice.call($.trim(str).split(/\W+/), -1);
            },
            prefetch: '/api/commands'
        });

        initTabKeyed();

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
