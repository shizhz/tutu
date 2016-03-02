String.prototype.hashCode = function() {
    var hash = 0, i, chr, len;
    if (this.length === 0) return hash;
    for (i = 0, len = this.length; i < len; i++) {
        chr   = this.charCodeAt(i);
        hash  = ((hash << 5) - hash) + chr;
        hash |= 0; // Convert to 32bit integer
    }
    return hash;
};

var TutuWebSocket = TutuWebSocket || (function() {
    var ws = undefined;
    var topicRegistry = {};

    function initTopics() {
        onTopic('cmd_result', function(data) {
            Tutu.addMsgForTutu(data);
        });
        onTopic('ws_close', function() {
            Tutu.addMsgForTutu({
                "shareCode": "",
                "message": "The connection seems closed, please refresh your browser to re-connect"
            });
        });
        onTopic('ws_error', function() {
            Tutu.addMsgForTutu({
                "shareCode": "",
                "message": "Some error seems just happened, please retry or refresh your browser"
            });
        });
        onTopic('ws_open', function(data) {
            Tutu.addMsgForTutu({
                "shareCode": "",
                "message": "Available commands: " + data['message']
            });
        });
        onTopic('share', function(data) {
            var shareCode = data['shareCode'];
            Tutu.addMsgForUser({
                "shareCode": shareCode,
                "message": data['cmd']
            });
            Tutu.addMsgForTutu({
                "shareCode": shareCode,
                "message": data['message']
            });
        });
        onTopic("internal_error", function(data) {
            Tutu.addMsgForTutu({
                "shareCode": "",
                "message": data['message']
            });
        });
    }

    function init() {
        if (!ws) {
            ws = new WebSocket("ws://" + location.host +  "/ws/invoke");
            ws.onmessage = function(evt) {
                var result = JSON.parse(evt.data);
                var topic = result['topic'];
                topicRegistry[topic]({
                    "cmd": result['cmd'],
                    "shareCode": result['share_code'],
                    "message": result['data']
                });
            };
            ws.onclose = function(evt) {
                topicRegistry['ws_close']();
            };
            ws.onerror = function(evt) {
                topicRegistry['ws_error']();
            };
            ws.onopen = function() {
                if (Cookies.get('share_code')) {
                    var shareCode = Cookies.get('share_code');
                    var cmd = "share " + shareCode;
                    Cookies.remove('share_code');
                    send({
                        'shareCode': cmd.hashCode(),
                        'command': cmd
                    });
                }
            };
        }
        initTopics();
    }

    function onTopic(topic, func) {
        topicRegistry = topicRegistry || {};
        topicRegistry[topic] = func;
    }

    function send(msg) {
        ws.send(JSON.stringify(msg));
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

    function addMsgForTutu(data) {
        addMessage({
            user: "Tutu",
            uicon: "tutu_icon",
            shareCode: data['shareCode'],
            content: data['message']
        });
    }

    function addMsgForUser(data) {
        addMessage({
            user: "You",
            uicon: "user_icon",
            shareCode: data['shareCode'],
            content: data['message']
        });
    }

    function addMessage(ctx) {
        if (ctx['shareCode']) {
            ctx['shareLink'] = "http://" + location.host + '/share/' + ctx['shareCode'];
        }
        var msgsDiv = $('#msgs_div');
        var template = Handlebars.compile($('#message_tmpl').html());

        function shareLink(container) {
            return $('a[share-link*="share"]', container).attr('share-link');
        }

        function hasShareLink(container) {
            return !!shareLink(container);
        }

        var tmpl = $(template(ctx)).hide().appendTo(msgsDiv).fadeIn(500).hover(function() {
            if (hasShareLink($(this))) {
                var ci = $('a[class*="copy_icon"]', $(this));
                ci.removeClass('hidden');
            }
        }, function() {
            if (hasShareLink($(this))) {
                $('a[class*="copy_icon"]', $(this)).addClass('hidden');
            }
        });

        if (ctx['shareCode']) {
            var ci = $('a[class*="copy_icon"]', tmpl);
            new Clipboard(ci[0], {
                text: function(trigger) {
                    return trigger.getAttribute('share-link');
                }
            });
        }

        var msgsScrollDiv = $('#msgs_scroller_div');
        msgsScrollDiv.animate({
            scrollTop: msgsScrollDiv.prop('scrollHeight')
        }, "slow");
    }

    function initHotkeyBindings() {
        var msg_box = $('#message-input')[0];

        Mousetrap(msg_box).bind('enter', function(e) {
            removeSuggestionMenu();
            if (!suggestionMenuVisible()) {
                var cmd = rawInput();
                var shareCode = cmd.hashCode();
                addMsgForUser({
                    "shareCode": shareCode,
                    "message": cmd
                });
                clearInput();
                TutuWebSocket.send({
                    "shareCode": shareCode,
                    "command": cmd
                });
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
        'addMessage': addMessage,
        'addMsgForTutu': addMsgForTutu,
        'addMsgForUser': addMsgForUser
    };
})();
