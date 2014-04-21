class @Flash
  element: 'flash_message'
  obj: null

  constructor: (element)->
    if element?
      @element = element
    @init()

  init: () ->
    $("<div id='#{@element}'></div>").appendTo('body')
    @obj = $('#' + @element)
    @obj.show()

  insert: (message, level) ->
    if not level?
      level = 'message'
    e = $("<div class='flash_item #{level}'>#{message}</div>").appendTo @obj
    window.setTimeout ()->
      $(e).hide(300)
    , 2000

    window.setTimeout ()->
      $(e).detach()
    , 2300

