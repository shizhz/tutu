var TutuWebSocket = TutuWebSocket || (function() {
    var ws = undefined;
    var topicRegistry = {};

    function initTopics() {
        onTopic('cmd_result', function(data) {
            Tutu.addMessage({
                user: "Tutu",
                uicon: "tutu_icon",
                content: data
            });
        });
        onTopic('ws-closed', function() {
            Tutu.addMessage({
                user: "Tutu",
                uicon: "tutu_icon",
                content: "The connection seems closed, please refresh your browser to re-connect"
            });
        });
        onTopic('ws-error', function() {
            Tutu.addMessage({
                user: "Tutu",
                uicon: "tutu_icon",
                content: "Some error seems just happened, please retry or refresh your browser"
            });
        });
    }

    function init() {
        if (!ws) {
            ws = new WebSocket("ws://" + location.host +  "/ws/invoke");
            ws.onmessage = function(evt) {
                var result = JSON.parse(evt.data);
                var topic = result['topic'];
                topicRegistry[topic](result['data']);
            };
            ws.onclose = function(evt) {
                topicRegistry['ws-closed']();
            };
            ws.onerror = function(evt) {
                topicRegistry['ws-error']();
            };
        }
        initTopics();
    }

    function onTopic(topic, func) {
        topicRegistry = topicRegistry || {};
        topicRegistry[topic] = func;
    }

    function send(msg) {
        ws.send(msg);
    }

    return {
        "init": init,
        "onTopic": onTopic,
        "send": send
    };
})();


var Tutu = Tutu || (function() {
    function rawInput() {
        return $('#message-input').val();
    };

    function clearInput() {
        return $('#message-input').val('');
    };

    function setSuggestedInput(sInput) {
        $('.typeahead').typeahead('val', sInput);
    };

    function suggestionMenuVisible() {
        return $('div.tt-menu').is(":visible");
    }

    function buildSuggestionCmd(rawInput, suggestion) {
        var cmdSegs = rawInput.split(/\W+/);
        return $.trim([].slice.call(cmdSegs, 0, -1).concat([suggestion]).join(' '));
    }

    function removeSuggestionMenu(e) {
        if (suggestionMenuVisible()) {
            var suggestions = $('div.tt-menu div.tt-suggestion');

            if (suggestions.length == 1) {
                var cmdSegs = rawInput().split(/\W+/);
                var lastCmdSeg = $.trim(cmdSegs[cmdSegs.length - 1]);
                var suggestion = $.trim(suggestions.text());
                if (lastCmdSeg == suggestion) {
                    setSuggestedInput(buildSuggestionCmd(rawInput(), suggestion));
                    $('.typeahead').typeahead('close');
                }
            }
        }
    }

    function addMessage(ctx) {
        var template = Handlebars.compile($('#message_tmpl').html());
        $(template(ctx)).hide().appendTo($('#msgs_div')).fadeIn(500);
    }

    function initHotkeyBindings() {
        var msg_box = $('#message-input')[0];

        Mousetrap(msg_box).bind('enter', function(e) {
            removeSuggestionMenu();
            if (!suggestionMenuVisible()) {
                var cmd = rawInput();
                addMessage({
                    user: "You",
                    uicon: "user_icon",
                    content: cmd
                });
                clearInput();
                TutuWebSocket.send(cmd);
            }
        });

        Mousetrap(msg_box).bind(['alt+backspace'], function() {
            setSuggestedInput(buildSuggestionCmd(rawInput(), ''));
        });
    }

    function initTypeahead() {
        var initTabKeyed = function() {
            var rInput;
            $('.typeahead').bind('typeahead:beforeselect typeahead:beforeautocomplete', function(e, suggestion) {
                rInput = rawInput();
            });

            $('.typeahead').bind('typeahead:select typeahead:autocomplete', function(e, suggestion) {
                setSuggestedInput(buildSuggestionCmd(rInput, suggestion.name));
            });
        };

        var initSuggestionEngine = function() {
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
            });
        };

        initTabKeyed();
        initSuggestionEngine();
    }

    function initFocus() {
        $('#message-input').focus();
    }

    $(function() {
        TutuWebSocket.init();
        initHotkeyBindings();
        initTypeahead();
        initFocus();
    });

    // API
    return {
        'addMessage': addMessage
    };
})();
