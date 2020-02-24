
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

function createSidebar(data) {
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
config.PLAY_BUTTON_HTML = '<span class="play-button"><img src="' + config.play_icon_url + '"/></span>';

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
    $('#sidebar').html(createSidebar(data));
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
  node.val(keyword.replace(/\+/g, '%20'));
  node.trigger('input');
}

$.getJSON(
  config.search_data_json_url,
  function(data) {
    var options = {
      threshold: 0.3,
      minMatchCharLength: 3,
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
      clearTimeout(timer);
      const _this = $(this);
      timer = setTimeout(function() {
        var result = fuse.search(_this.val());
        renderSearchResult(config, result);
        initLazy();
      }, 200);
    });
    if (keyword) {
      node.trigger('input');
    }

  }
);

}

function renderSearchResult(config, result) {
  const html = result.map(function(v){
    return $('<div/>')
        .addClass('video-item vid-col col-xl-2 col-lg-3 col-sm-4')
        .append(renderVid(config, v));
  }) 
  $('#search-result').empty().append(html);
}

