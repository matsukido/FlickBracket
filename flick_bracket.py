import sublime
import sublime_plugin

import itertools as itools


class FlickBracketCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        vw = self.view
        carretpt = vw.sel()[0].b
        char = vw.substr(carretpt)

        if char in ")]}>":
            rng = range(carretpt + 1, carretpt + 99)
            sp = itools.dropwhile(lambda pt: vw.substr(pt).isspace(), rng)
            rgn = sublime.Region(carretpt, next(sp))
            # print(rgn)
            vw.erase(edit, rgn)
            vw.insert(edit, vw.line(carretpt).end(), char)
            # (lll))))>