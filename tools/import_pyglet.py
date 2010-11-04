* check out the latest pyglet trunk
* copy it to a new aptana project
* do a search and replace for
" pyglet" -> " fos.lib.pyglet"
"(pyglet" -> "(fos.lib.pyglet"
"@pyglet" -> "@fos.lib.pyglet"
In pyglet.__init__, line number 312
'pyglet.%s' -> 'fos.lib.pyglet.%s'
* copy the pyglet folder into fos/lib