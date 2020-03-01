const SHOW_PLAY_ICON = false;

function createSidebarGroup(id, cls, items) {
  const ul = $('<ul class="list-group" />').addClass(cls).attr('id', id);
  const lis = $.map(items, function(item) {
    const li = $('<li />').addClass('list-group-item');
    const badge = item.video_count > 0 
        ? $('<span class="badge badge-dark ml-1"></span>').text(item.video_count)
        : null;
    const a = $('<a />')
        .addClass("d-flex justify-content-between align-items-center")
        .attr('href', item.url)
        .text(item.title)
        .append(badge);
    return li.append(a);
  });
  return ul.append(lis);
}

function createLeftSidebar(data) {
  const toggle = $('<a class="lang-toggle collapsed" data-toggle="collapse" href="#secondaryLangsMenu" role="button" aria-expanded="false" />');
  const wrapper = $('<div />')
      .append(createSidebarGroup('lang-nav', '', data.top_langs))
      .append(toggle)
      .append(
        $('<div />')
            .addClass('collapse')
            .attr('id', 'secondaryLangsMenu')
            .append(createSidebarGroup('secondary-lang-nav', '', data.secondary_langs)))
      .append($('<hr/>'))
      .append(createSidebarGroup('topic-nav', '', data.topics))
  return wrapper;
}

function createRightSidebarItem(x) {
  const html = [
    '<a href="', x.url, '">',
    '<div class="media">',
    '<div class="mr-3 thumb-outter-container">',
      '<div class="thumb-container">',
      '<div class="thumb-wrapper">',
      '<img src="', x.thumbnail_url, '" />',
      '</div>',
      '</div>',
    '</div>',
    '<div class="media-body">',
      '<div class="title">', x.title, '</div>',
      '<div>', x.meta1, '</div>',
    '</div>',
    '</div>', // media
    '</a>',
  ];

  return html.join('');
}

function shuffle_list(list, size) {
  const N = list.length;
  for (let i = 0; i < size; i++) {
    let j = Math.floor(Math.random() * (N - i));
    let t = list[i];
    list[i] = list[j];
    list[j] = t;
  }
  return list.slice(0, size);
}

function createRightSidebar(data) {
  const featured_contents = shuffle_list(data.featured_contents, 5);
  let html = [];
  const block1 = featured_contents.map(x => createRightSidebarItem(x));
  const block2 = data.recent_weeks.map(x => createRightSidebarItem(x));

  html.push('<h5>Featured contents</h5>');
  html = html.concat(block1);
  html.push('<h5>Weekly archives</h5>');
  html = html.concat(block2);
  return html.join('');
}

function getUrlVars() {
  var vars = {};
  var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
      vars[key] = value;
  });
  return vars;
}

function link(title, url) {
  return ['<a href="',url,'">',title,'</a>'].join('');
}

function renderVid(config, vid) {
  return html = [
      '<div class="vid">',
      '<div class="thumb-container">',
      '<div class="thumb-wrapper">',
      '<a target="_blank" href="',
      vid.video_url,
      '"><img data-src="',vid.thumbnail_url,'"/>',
      config.PLAY_BUTTON_HTML,
      '</a>',
      '</div>',
      '<div class="thumb-label">',
      vid.duration,
      '</div>',
      '</div>',
      '<div class="title">',
       link(vid.title, vid.video_url),
       '</div>',
      '<div class="meta">',
      link(vid.channel_title, vid.channel_url),
      '&nbsp;&bull;&nbsp;',
      vid.published_at,
      '</div>',
      '</div>',
      ].join('');
}

function initLazy() {
$('.thumb-container img').Lazy({
  effect: 'fadeIn',
  effectTime: 200,
  visibleOnly:true,
})
}

function initPage(config) {
config.PLAY_BUTTON_HTML = '';
if (SHOW_PLAY_ICON) {
  config.PLAY_BUTTON_HTML = '<span class="play-button"><img src="' + config.play_icon_url + '"/></span>';
}

$('.video-item').each(function(i, e){
  e = $(e);
  data = {
    channel_title: e.attr('data-channel-title'),
    channel_url: e.attr('data-channel-url'),
    duration: e.attr('data-duration'),
    published_at: e.attr('data-published-at'),
    thumbnail_url: e.attr('data-thumbnail-url'),
    title: e.attr('data-title'),
    video_url: e.attr('data-video-url'),
  }
  const v = renderVid(config, data)
  e.append(v)
});

initLazy();

$.getJSON(
  config.nav_json_url,
  function(data) {
    $('#sidebar').html(createLeftSidebar(data.nav));
    $('#right-sidebar').html(createRightSidebar(data));
  }
);

$("#sidebar-toggle").click(function(e) {
  e.preventDefault();
  $("#wrapper").toggleClass("toggled");
});

};

// Search

function initSearch(config) {
const node = $('#search-keyword');
const queryString = window.location.search;
const params = new URLSearchParams(queryString);
const keyword = params.get("keyword");
if (keyword) {
  node.val(keyword.replace(/\+/g, '%20').trim());
  node.trigger('input');
}

$.getJSON(
  config.search_data_json_url,
  function(data) {
    var options = {
      shouldSort: true,
      threshold: 0.1,
      minMatchCharLength: 3,
      maxPatternLength: 32,
      keys: [
        "title",
        "channel_title",
        "metadata",
      ],
    };
    var fuse = new Fuse(data, options);

    node.removeAttr('readonly');
    node.focus();

    var timer;
    node.on('input', function(){
      clearSearchResult();
      clearTimeout(timer);
      const _this = $(this);
      timer = setTimeout(function() {
        var result = fuse.search(_this.val().trim());
        renderSearchResult(config, result);
        initLazy();
      }, 500);
    });
    if (keyword) {
      node.trigger('input');
    }

  }
);

}

function renderSearchResult(config, result) {
  const html = result.slice(0, 30).map(function(v){
    return $('<div/>')
        .addClass('video-item vid-col col-xl-2 col-lg-3 col-sm-4')
        .append(renderVid(config, v));
  }) 
  $('#search-result').empty().append(html);
}

function clearSearchResult() {
  $('#search-result').empty();
}

