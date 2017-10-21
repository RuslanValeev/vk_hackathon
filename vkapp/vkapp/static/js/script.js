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

function renderMatch(data) {
    var matchTemplate = _.template($('#match_template').html());
    return $(matchTemplate(data));
}

function showMatch(name) {
    if (!name)
        return
    var newMatch = renderMatch(name);
    newMatch.addClass('showing').prependTo($('#match_wrapper'));
    _.delay(function () {
        newMatch.removeClass('showing');
    }, 15)
}

$(document).ready(function () {
    var tabs = $('#menu a[data-toggle-href]');
    tabs.click(function (event) {
        var tab_name = $(this).attr('data-toggle-href');
        switchTab(tab_name)
    });
    switchTab('match_list');
    showMatch(testUsers.pop());

    var eventList = $('#event_list');

    $.ajax({
        url: '/get_events?limit=20',
        success: function (events) {
            events.forEach(function (event, index) {
                eventList.append(renderEvent(event));
            });
        }
    });
    $("#deny_button").click(function () {
            $('#match_wrapper').find('.card').addClass('denying');
            showMatch(testUsers.pop());
        }
    );

    $('#allow_button').click(function () {
            $('#match_wrapper').find('.card').addClass('allowing');
            showMatch(testUsers.pop());
    });

    // $("#tinderslide").jTinder();
    // testDataJson.forEach(function (event, index) {
    //     eventList.append(renderEvent(event));
    // });

});