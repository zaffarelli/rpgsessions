class Scheduler {
    constructor() {
        // this.d3 = undefined;
        this.init();
    }

    init() {
        let me = this;
        me.prepare_ajax();
    }

    prepare_ajax() {
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    let csrf_middlewaretoken = $('input[name=csrfmiddlewaretoken]').val();
                    xhr.setRequestHeader('X-CSRFToken', csrf_middlewaretoken);
                }
            }
        });
    }

    revealUI() {
        let me = this;
        $('.menuzone').removeClass('hidden');
        $('.eventzone').removeClass('hidden');
        $('.userzone').removeClass('hidden');
        $('.wrapper').removeClass('hidden');
    }

    hideUI() {
        let me = this;
        $('.menuzone').addClass('hidden');
        $('.eventzone').addClass('hidden');
        $('.userzone').addClass('hidden');
        $('.wrapper').addClass('hidden');
    }


    revealLog() {
        let me = this;
        // $('.menuzone').addClass('hidden');
        // $('.eventzone').addClass('hidden');
        // $('.userzone').addClass('hidden');
        // $('.wrapper').addClass('hidden');
        $('.adminzone').removeClass('hidden');
    }

    registerDisplay() {
        let me = this;
        $('.display').off().on('click', function (event) {
            let action = $(this).attr('action');
            let param = $(this).attr('param');
            let option = $(this).attr('option');
            // console.log(action+"|"+param+"|"+option)
            let key = $('#userinput').val();
            let url = 'ajax/display/' + action + '/';
            if (param != undefined) {
                let p = param.replaceAll('-', '_');
                if (option) {
                    url = 'ajax/display/' + action + '/' + p + '/' + option + '/';
                } else {
                    url = 'ajax/display/' + action + '/' + p + '/';
                }
            }
            $.ajax({
                url: url,
                success: function (answer) {
                    if (action == 'session_details') {
                        $('.day_details').html(answer.data)
                    } else {
                        $('.wrapper').html(answer.data)
                    }
                    $('.menuzone').html(answer.menu)
                    me.rebootLinks();
                },
                error: function (answer) {
                    console.error(answer);
                    me.rebootLinks();
                },
            });
        });
    }

    registerOverlay() {
        let me = this;
        $('.modal_switch').off().on('click', function (event) {
            let action = $(this).attr('action');
            let param = $(this).attr('param');
            let option = $(this).attr('option');
            $('#callback').html("");
            let url = 'ajax/overlay/' + action + '/';
            if (param != undefined) {
                let p = param.replaceAll('-', '_');

                if (option) {
                    url = 'ajax/overlay/' + action + '/' + p + '/' + option + '/';
                } else {
                    url = 'ajax/overlay/' + action + '/' + p + '/';
                }
            }
            $.ajax({
                url: url,
                success: function (answer) {
                    if (action == 'close') {
                        $('#overlay').addClass('hidden');
                        $('#dialog').html("Nope");
                    } else {

                        console.log(answer.data)
                        $('#dialog').html(answer.data);
                        $('#overlay').removeClass('hidden');
                        // $('#callback').html(answer.callback);
                    }
                    me.rebootLinks();
                },
                error: function (answer) {
                    console.error(answer);
                    me.rebootLinks();
                },
            });
        });
    }

    registerToggle() {
        let me = this;
        $('.toggle').off().on('click', function (event) {
            event.preventDefault();
            event.stopPropagation();
            let action = $(this).attr('action');
            let param = $(this).attr('param');
            let option = $(this).attr('option');
            let url = 'ajax/toggle/' + action + '/';
            if (param != undefined) {
                let p = param.replaceAll('-', '_');
                if (option) {
                    url = 'ajax/toggle/' + action + '/' + p + '/' + option + '/';
                } else {
                    url = 'ajax/toggle/' + action + '/' + p + '/';
                }
            }
            $.ajax({
                url: url,
                success: function (answer) {
                    if (action == 'toggle_follower') {
                        $('#dialog').html(answer.data);
                    } else {
                        $(answer.target).html(answer.data);
                    }
                    me.rebootLinks();
                },
                error: function (answer) {
                    console.error(answer);
                    me.rebootLinks();
                }
            });

        });
    }

    registerAction() {
        let me = this;
        $('.action').off().on('click', function (event) {
            event.preventDefault();
            event.stopPropagation();
            let action = $(this).attr('action');
            let param = $(this).attr('param');
            let option = $(this).attr('option');
            let url = 'ajax/action/' + action + '/';

            // if (action == 'submit') {
            //     document.forms[param].submit();
            // }

            let formdata = $(param).serialize();
            let tgt = $('.character_form').attr('form-target');

            $.ajax({
                url: 'ajax/action/new_session/' + id + '/',
                type: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                data: formdata,
                dataType: 'json',
                success: function (answer) {
                    $('#tile_back_' + id).click();
                    me.rebootLinks();
                },
                error: function (answer) {
                    console.log(answer.responseText);
                },
            });


            // if (param != undefined) {
            //     let p = param.replaceAll('-', '_');
            //     if (option) {
            //         url = 'ajax/toggle/' + action + '/' + p + '/' + option + '/';
            //     } else {
            //         url = 'ajax/toggle/' + action + '/' + p + '/';
            //     }
            // }
            // $.ajax({
            //     url: url,
            //     success: function (answer) {
            //         if (action == 'submit') {
            //             $('#'+param).submit();
            //             $('#dialog').html(answer.data);
            //         } else {
            //             $(answer.target).html(answer.data);
            //         }
            //         me.rebootLinks();
            //     },
            //     error: function (answer) {
            //         console.error(answer);
            //         me.rebootLinks();
            //     }
            // });

        });
    }


    rebootLinks() {
        let me = this;
        _.defer(function () {
            me.registerDisplay();
            me.registerOverlay();
            me.registerToggle();
            me.registerAction();
        });
    }

    perform() {
        let me = this;
        // me.loadAjax();
        me.rebootLinks();
    }

}


















