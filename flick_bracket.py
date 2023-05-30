import sublime
import sublime_plugin

import itertools as itools


class FlickBracketCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        vw = self.view
        caretrgn = vw.sel()[0]
        caretpt = caretrgn.end()
        lineend = vw.line(caretpt).end()

        itrng = iter(range(caretpt, lineend + 1))
        preds = [lambda pt: vw.substr(pt) not in ")]}>",
                 lambda pt: vw.substr(pt) in ")]}>",
                 lambda pt: vw.substr(pt) in " \t"]

        drops = map(itools.dropwhile, preds, [itrng] * 3)
        bracket, bracketend, erasept = list(map(next, drops, [lineend] * 3))

        if bracket == lineend:
            return

        movestr = vw.substr(sublime.Region(caretpt, bracketend))

        vw.erase(edit, sublime.Region(caretpt, erasept))

        linergns = iter(vw.lines(sublime.Region(caretpt, caretpt + 1500)))
        if vw.classify(caretpt) & sublime.CLASS_LINE_END:
            next(linergns)

        flickers = ("(", "[", "{", "<", ",")
        nonconmma = itools.dropwhile(
                        lambda rgn: vw.substr(rgn).rstrip().endswith(flickers),
                        linergns)

        vw.insert(edit, next(nonconmma, caretrgn).end(), movestr)