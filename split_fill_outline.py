#!/usr/bin/env python3
"""
Split Fill and Outline

Duplicates each selected object: outline only on the copy on top, fill only
on the original on the bottom. For a group, every object inside it is
changed the same way.
"""
import inkex
from inkex import EffectExtension, ShapeElement, Group

SVG_NS = inkex.NSS['svg']
DRAWN = {f'{{{SVG_NS}}}{t}' for t in
         ('path', 'rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'text', 'use')}


def set_everywhere(node, prop):
    """Set prop to none on node and on every drawn object inside it."""
    for el in node.iter():
        if not isinstance(el.tag, str):
            continue
        if el is node or el.tag in DRAWN or isinstance(el, Group):
            el.style[prop] = 'none'


class SplitFillOutline(EffectExtension):

    def effect(self):
        chosen = [el for el in self.svg.selection.values() if isinstance(el, ShapeElement)]
        if not chosen:
            raise inkex.AbortExtension('Select one or more objects first.')
        # An object inside a selected group is handled with its group.
        ids = {id(el) for el in chosen}
        chosen = [el for el in chosen
                  if not any(id(a) in ids for a in el.iterancestors())]
        for el in chosen:
            top = el.duplicate()        # placed directly above the original
            set_everywhere(top, 'fill')
            set_everywhere(el, 'stroke')


if __name__ == '__main__':
    SplitFillOutline().run()
