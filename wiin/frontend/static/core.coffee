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

  insert: (message, level) ->
    if not level?
      level = 'message'
    @obj.append(
      "<div class='flash_item #{level}'>#{message}</div>"
    )

