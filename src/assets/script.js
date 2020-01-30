
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

function div(cls) {
  return $('<div/>').addClass(cls);
}

function link(title, url) {
  return $('<a/>').attr('href', url).text(title);
}

function initPage(config) {

$('.video-item').each(function(i, e){
  e = $(e);
  const playButton = $('<span/>')
      .addClass('play-button')
      .append($('<img />').attr('src', config.play_icon_url));
  const a = link('', e.attr('data-video-url'))
      .attr('target', '_blank')
      .append($('<img/>').attr('data-src', e.attr('data-thumbnail-url')))
      .append(playButton)
      ;
  const tw = div('thumb-wrapper').append(a);
  const duration = div('thumb-label').text(e.attr('data-duration'));
  const tc = div('thumb-container').append([tw, duration]);
  const title = div('title')
      .append(link(e.attr('data-title'), e.attr('data-video-url')));
  const meta = div('meta')
      .append(link(e.attr('data-channel-title'), e.attr('data-channel-url')))
      .append("&bull;")
      .append(e.attr('data-published-at'));
  const vid = div('vid').append([tc,title,meta]);
  e.append(vid)
});

$('.thumb-container img').Lazy({
  effect: 'fadeIn',
  effectTime: 200,
  visibleOnly:true,
})

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

