var testDataJson = [
    {
        event_id: 1,
        title: 'Бегущий по лезвию',
        image_url: 'https://img06.rl0.ru/afisha/e1120x-q80i/s1.afisha.ru/MediaStorage/95/5f/40281b9513ba44d2b093993b5f95.jpg',
        subscribers: 100,
        wall_id: '151168842_3',
        start_date: 1508505843751,
        description: "Сиквел фантастического шедевра 1982 года «Бегущий по лезвию», который под отеческим присмотром Ридли Скотта и по сценарию Майкла Грина («Чужой: Завет», «Американские боги») снял отличный канадский режиссер Дени Вильнев («Убийца»», «Прибытие»). Сюжет ра..."
    },
    {
        event_id: 1,
        title: 'Второй фильм',
        image_url: 'https://img06.rl0.ru/afisha/e1120x-q80i/s1.afisha.ru/MediaStorage/95/5f/40281b9513ba44d2b093993b5f95.jpg',
        subscribers: 100,
        wall_id: '151168842_3',
        start_date: 1508505843751,
        description: "Сиквел фантастического шедевра 1982 года «Бегущий по лезвию», который под отеческим присмотром Ридли Скотта и по сценарию Майкла Грина («Чужой: Завет», «Американские боги») снял отличный канадский режиссер Дени Вильнев («Убийца»», «Прибытие»). Сюжет ра..."
    },
    {
        event_id: 1,
        title: 'Бегущий по лезвию',
        image_url: 'https://img06.rl0.ru/afisha/e1120x-q80i/s1.afisha.ru/MediaStorage/95/5f/40281b9513ba44d2b093993b5f95.jpg',
        subscribers: 100,
        wall_id: '151168842_3',
        start_date: 1508505843751,
        label: 'like',
        description: "Сиквел фантастического шедевра 1982 года «Бегущий по лезвию», который под отеческим присмотром Ридли Скотта и по сценарию Майкла Грина («Чужой: Завет», «Американские боги») снял отличный канадский режиссер Дени Вильнев («Убийца»», «Прибытие»). Сюжет ра..."
    },
    {
        event_id: 1,
        title: 'Бегущий по лезвию',
        image_url: 'https://img06.rl0.ru/afisha/e1120x-q80i/s1.afisha.ru/MediaStorage/95/5f/40281b9513ba44d2b093993b5f95.jpg',
        subscribers: 100,
        wall_id: '151168842_3',
        start_date: 1508505843751,
        label: 'fire',
        description: "Сиквел фантастического шедевра 1982 года «Бегущий по лезвию», который под отеческим присмотром Ридли Скотта и по сценарию Майкла Грина («Чужой: Завет», «Американские боги») снял отличный канадский режиссер Дени Вильнев («Убийца»», «Прибытие»). Сюжет ра..."
    },
];
var testUsers = [
    {
        avatar_url: 'https://cs5.pikabu.ru/post_img/big/2014/08/21/5/1408603111_2145351416.jpg',
        name: 'Emma'
    },
    {
        avatar_url: 'https://chivethethrottle.files.wordpress.com/2012/05/girlllllllllls-920-20.jpg?w=920&h=940',
        name: 'Olivia'
    },
    {
        avatar_url: 'https://chivethebrigade.files.wordpress.com/2012/06/bad-idea-06_22_12-920-5.jpg',
        name: 'Rachel Maddaw'
    },
    {
        avatar_url: 'https://pbs.twimg.com/profile_images/556715565398519808/22TRbE-V.jpeg',
        name: 'Charlotte Musk'
    },
    {
        avatar_url: 'http://desktopwallpapers.org.ua/download.php?img=201302/1024x1024/desktopwallpapers.org.ua-24821.jpg',
        name: 'Khaleesi Gates'
    },
    {
        avatar_url: 'http://www.kartinki.me/pic/201204/1024x1024/kartinki.me-3445.jpg',
        name: 'Bathsheba Putin'
    }
];
var users_info = [
    {
        id: 1,
        avatar_url: "https://pp.userapi.com/c630029/v630029117/4cd13/9s7ea6GLnbs.jpg",
        name: "Назаров Тимофей",
        description: "Пацан с хакатона, тёлки, добавляйтесь!",
        sex: 'male',
        age: '21'       //ну и там сам че найдешь - присылай
    }
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
    processedData['label'] = data['label'] ? labelTemplate({icon: data['label']}) : '';
    processedData['event_id'] = data['creation_id'];
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
    var matchTemplate = _.template($('#user_card_template').html());
    processedData['name'] = data['first_name'];
    processedData['avatar_url'] = data['photo_400_orig'];
    processedData['user_id'] = data['id'];
    return $(matchTemplate(processedData));
}

function renderMatch(data) {
    var matchTemplate = _.template($('#match_card_template').html());
    return $(matchTemplate(data));
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
    showUserCard(users.pop());
    $('#modal_user_cards').modal({
        onHide: function () {
            $(window).off('keydown');
            getMatches(function (data) {
                $('#new_matches_counter').text(_.size(data.response)).show();
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
    $(this).addClass('disabled');
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
        url: '/get_events?limit=20&type=concert&user_id=' + window.user_id,
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
            users.forEach(function (user) {
                $('#match_list').find('.ui.grid.centered').append(renderMatch(user));
            })
        });
    });

});