#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import with_statement

import os
import sys
import appuifw
import graphics
import sysinfo


class MedCalc(object):
    def run(self):
        flags = appuifw.FFormEditModeOnly + appuifw.FFormDoubleSpaced
        self._f = appuifw.Form(self.data, flags)
        self._f.save_hook = self.mark_saved
        self._f.flags = appuifw.FFormEditModeOnly + appuifw.FFormDoubleSpaced
        self._f.execute()

    def mark_saved(self, aBool):
        self._saved = aBool

    def getform(self):
        return self._f

    def is_saved(self):
        return self.bmi_saved


class MedCalcList(object):
    # Formato Checkbox
    def run(self):
        self._f = appuifw.multi_selection_list(
            self.data, style='checkbox', search_field=1)

    def mark_saved(self, aBool):
        self._saved = aBool

    def getform(self):
        return self._f

    def is_saved(self):
        return True


class MedCalcMQ(object):
    # Formato Multi Questionario
    def run(self):
        self._f = appuifw.multi_selection_list(
            self.data, style='checkbox', search_field=1)

    def mark_saved(self, aBool):
        self._saved = aBool

    def getform(self):
        return self._f

    def is_saved(self):
        return True


class MedImage(object):
    def run(self):
        possible_locations = []
        possible_locations.append(os.path.join(sys.path[0], self.fname))
        possible_locations.append(self.fname)
        possible_locations.append(os.path.join('c:\\data\\python\\', self.fname))
        possible_locations.append(os.path.join('c:\\data\\python\\medcalc\\', self.fname))

        appuifw.app.screen = 'full'
        for location in possible_locations:
            if os.path.exists(location):
                try:
                    img1 = graphics.Image.open(location)
                    a = sysinfo.display_pixels()
                    if (a[1] / a[0] >= 1):
                        # Not sure about transpose type
                        img1 = img1.transpose('ROTATE_90')
                except:
                    pass

        def handle_redraw(rect):
            canvas.blit(img1)

        canvas = appuifw.Canvas(redraw_callback=handle_redraw)
        try:
            canvas.blit(img1)
            appuifw.app.body = canvas
        except:
            appuifw.note(u"Error img1", "note")

    def mark_saved(self, aBool):
        self._saved = aBool

    def getform(self):
        return self._f


class MenuFilho:
    """Menu."""
    def run(self, menupai):
        from key_codes import EKeyLeftArrow
        self.lb = appuifw.Listbox(self.Children, self.lbox_observe)
        self.lb.bind(EKeyLeftArrow, lambda: self.lbox_observe(0))
        appuifw.app.title = self.Title
        appuifw.app.menu = []
        appuifw.app.exit_key_handler = self.exit_key_handler
        appuifw.app.body = self.lb
        self.menupai = menupai

    def lbox_observe(self, ind=None):
        if ind is not None:
            index = ind
        else:
            index = self.lb.current()
        focused_item = 0
        self.MenuKid[index].run()
        self.MenuKid[index].show()
        appuifw.app.screen = 'normal'

    def exit_key_handler(self):
        appuifw.app.exit_key_handler = None
        self.menupai.refresh()

    def do_exit(self):
        self.exit_key_handler()
