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
                 lambda pt: vw.substr(pt) in ")]}>"]

        drops = map(itools.dropwhile, preds, [itrng] * 2)
        bracket, bracketend = list(map(next, drops, [lineend] * 2))

        if bracket == lineend:
            return

        movestr = vw.substr(sublime.Region(caretpt, bracketend))

        rng = range(bracketend, lineend)
        erasept = next(itools.dropwhile(lambda pt: vw.substr(pt).isspace(), rng), None)
        if erasept is None:
            return
        vw.erase(edit, sublime.Region(caretpt, erasept))

        linergns = iter(vw.lines(sublime.Region(caretpt, caretpt + 1500)))
        if vw.classify(caretpt) & sublime.CLASS_LINE_END:
            next(linergns)

        flickers = ("(", "[", "{", "<", ",")
        nonconmma = itools.dropwhile(
                        lambda rgn: vw.substr(rgn).rstrip().endswith(flickers),
                        linergns)

        pt = next(nonconmma, caretrgn).end()
        rgn = vw.line(pt)
        txt = vw.substr(rgn)
        stripped = txt.rstrip()

        if stripped.endswith((";", ":")):
            pt -= (len(txt) - len(stripped) + 1)

        vw.insert(edit, pt, movestr)