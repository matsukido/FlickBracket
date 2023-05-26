import sublime
import sublime_plugin

import itertools as itools


class FlickBracketCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        vw = self.view
        carretrgn = vw.sel()[0]
        carretpt = carretrgn.end()
        char = vw.substr(carretpt)

        if char not in ")]}>":
            return

        rng = range(carretpt + 1, carretpt + 99)
        nonsp = itools.dropwhile(lambda pt: vw.substr(pt) in " \t", rng)
        pnt = next(nonsp, -1)
        if pnt == -1:
            return
        vw.erase(edit, sublime.Region(carretpt, pnt))

        linergns = iter(vw.lines(sublime.Region(carretpt, carretpt + 999)))
        if vw.classify(carretpt) & sublime.CLASS_LINE_END:
            next(linergns)

        nonconmma = itools.dropwhile(lambda rgn: vw.substr(rgn).rstrip().endswith(","), 
                                     linergns)
        vw.insert(edit, next(nonconmma, carretrgn).end(), char)
