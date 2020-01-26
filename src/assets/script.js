
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

function initPage(nav_json_url) {

$('.thumb-container img').Lazy({
  effect: 'fadeIn',
  effectTime: 200,
  visibleOnly:true,
})

$.getJSON(
  nav_json_url,
  function(data) {
    $('#sidebar').html(createSidebar(data));
  }
);

$("#sidebar-toggle").click(function(e) {
  e.preventDefault();
  $("#wrapper").toggleClass("toggled");
});

};

