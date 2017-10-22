var testUsers = [
    {
        photo_400_orig: 'https://cs5.pikabu.ru/post_img/big/2014/08/21/5/1408603111_2145351416.jpg',
        name: 'Emma'
    },
    {
        photo_400_orig: 'https://pbs.twimg.com/profile_images/556715565398519808/22TRbE-V.jpeg',
        name: 'Charlotte Musk'
    },
];

_.templateSettings = {
    interpolate: /\{\{=([\s\S]+?)\}\}/g,
};

function renderEvent(data) {
    var timeOptions = {
        hour: '2-digit',
        minute: 'numeric'
    };
    var dateOptions = {
        year: '2-digit',
        month: 'numeric',
        day: 'numeric',
        weekday: 'short'
    };

    var eventTemplate = _.template($('#event_template').html());
    var labelTemplate = _.template($('#event_label').html());

    processedData = _.pick(data, ['image_url', 'name']);
    var dateTime = new Date(data['begin'] || data['end']);

    processedData['time'] = dateTime.toLocaleString("ru", timeOptions);
    processedData['date'] = dateTime.toLocaleString("ru", dateOptions);
    processedData['description'] = (data['description'] || data['editorial_comment'] || data['synopsis'] || '').slice(0, 80);
    processedData['label'] = data['is_liked'] ? labelTemplate({icon: 'like'}) : '';
    processedData['event_id'] = data['creation_id'];
    processedData['likes'] = data['likes_counter'];
    processedData['liked'] = data['is_liked'] ? 'true' : 'false';
    return eventTemplate(processedData);
}

function switchTab(name) {
    var tabs = $('#menu a[data-toggle-href]');
    var thisTab = $('[data-toggle-href=' + name + ']');
    tabs.not(thisTab).removeClass('active');
    thisTab.addClass('active');

    var tab = $('#' + name);
    $('.toggled-tab').not(tab).hide();
    tab.show();
}

function renderUser(data) {
    var userTemplate = _.template($('#user_card_template').html());
    processedData['name'] = data['first_name'];
    processedData['avatar_url'] = data['photo_400_orig'];
    processedData['user_id'] = data['id'];
    return $(userTemplate(processedData));
}

function renderMatch(data) {
    var matchTemplate = _.template($('#match_card_template').html());
    processedData['name'] = data['first_name'];
    processedData['avatar_url'] = data['photo_400_orig'];
    // processedData['user_id'] = data['id'];
    return $(matchTemplate(processedData));
}

function getMatches(callback) {
    $.ajax({
        url: '/matching/get_matches',
        method: 'GET',
        data: {
            user_id: window.user_id
        },
        success: callback
    });
}

function getUsers(ids, callback) {
    VK.api("users.get", {
        "user_ids": ids.join(','),
        "fields": "sex,photo_400_orig,bdate,status,screen_name"
    }, callback);
}

function showUserCard(name) {
    if (!name) {
        _.delay(function () {
            $('#modal_user_cards').modal('hide');
        }, 400);
        return;
    }
    var newMatch = renderUser(name);
    newMatch.addClass('showing').prependTo($('#match_wrapper'));
    _.delay(function () {
        newMatch.removeClass('showing');
    }, 15)
}

function sendLike(like) {
    $.ajax({
        url: '/matching/like',
        method: 'POST',
        data: {
            user_id: window.user_id,
            event_id: sendLike.event_id,
            subject_id: $('#match_wrapper').find('.user_card').data('user-id'),
            like: like ? 'True' : 'False'
        }
    });
}

function denyUser(users) {
    sendLike(false);
    $('#match_wrapper').find('.card').addClass('denying')
        .one('transitionend webkitTransitionEnd oTransitionEnd', function () {
            $(this).remove();
        });
    showUserCard(users.pop());
}

function allowUser(users) {
    sendLike(true);
    $('#match_wrapper').find('.card').addClass('allowing')
        .one('transitionend webkitTransitionEnd oTransitionEnd', function () {
            $(this).remove();
        });
    showUserCard(users.pop())
}

function showModalUserCards(data) {
    var users = _.reject(data.response, function (user) {
        return user.id === window.user_id
    });
    if(_.isEmpty(users)) {
        return;
    }
    showUserCard(users.pop());
    $('#modal_user_cards').modal({
        onHide: function () {
            $(window).off('keydown');
            getMatches(function (data) {
                $('#new_matches_counter').text(_.chain(data).values().flatten().uniq().size().value() + 2).show();
            });
            $('#match_wrapper').find('.card').remove();
            $('#deny_button').add('#allow_button').off('click');

        },
        onShow: function () {
            $(window).on('keydown', function (event) {
                switch (event.originalEvent.key) {
                    case 'ArrowLeft':
                        denyUser(users);
                        break;
                    case 'ArrowRight':
                        allowUser(users);
                        break;
                }
                event.stopPropagation();
            });

            $("#deny_button").on('click', function () {
                denyUser(users);
            });
            $('#allow_button').on('click', function () {
                allowUser(users);
            });
        }
    }).modal('show');
}

function subscribeToEvent() {
    $.ajax({
        url: '/matching/subscribe',
        method: 'POST',
        data: {
            csrfmiddlewaretoken: CSRF_TOKEN,
            event_id: $(this).data('event-id'),
            user_id: window.user_id
        }
    });

    $.ajax({
        url: '/matching/get_subscribers',
        method: 'GET',
        data: {
            event_id: $(this).data('event-id'),
            user_id: window.user_id,
            filter: true
        },
        success: function (ids) {
            getUsers(ids.users, showModalUserCards);
        }
    });
    function updateCounter(counter) {
        var counterTemplate = _.template($('#counter_template').html());
        counter.replaceWith(counterTemplate({likes: parseInt(counter.data('counter')) + 1}));
    }
    if(!$(this).parents('.event').data('liked')) {
        updateCounter($(this).parent().find('.likes'))
    }
    $(this).parents('.event').data('liked', true);
    $(this).parents('.event').find('.ui.fluid.image').append(_.template($('#event_label').html())({icon: 'like'}));
    sendLike['event_id'] = $(this).data('event-id');
}

$(document).ready(function () {
    VK.init(function () {
        console.log('VK init success');
    }, function () {
        console.log('VK Init error');
    }, '5.68');
    window.user_id = parseInt(window.location.search.match(/viewer_id=(\d+)/)[1]);


    var tabs = $('#menu a[data-toggle-href]');
    tabs.click(function (event) {
        var tab_name = $(this).attr('data-toggle-href');
        switchTab(tab_name)
    });
    switchTab('event_list');

    var eventList = $('#event_list');

    $.ajax({
        url: '/get_events',
        data: {
            limit: 20,
            type: 'concert',
            user_id: window.user_id
        },
        success: function (events) {
            events.forEach(function (event, index) {
                eventList.append(renderEvent(event));
            });
            $('.subscribe_to_event').click(subscribeToEvent);
        }
    });

    getMatches(function (data) {
        //     data.response.forEach(function (user) {
        //     $('#match_list').find('.ui.grid.centered').append(renderMatch(user));
        // });
        getUsers(_.flatten(_.values(data)), function (data) {
            var users = _.reject(data.response, function (user) {
                return user.id === window.user_id
            });
            _.union(users, testUsers).forEach(function (user) {
                $('#match_list').find('.ui.grid.centered').append(renderMatch(user));
            })
        });
    });

});