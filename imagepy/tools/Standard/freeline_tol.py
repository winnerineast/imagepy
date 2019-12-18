# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 17:35:09 2016

@author: yxl
"""
from imagepy.core.roi import lineroi
import wx
from imagepy.core.engine import Tool

class Linebuf:
    """FreeLinebuf class"""
    title = 'Free Line'
    def __init__(self):
        self.buf = []
        
    def addpoint(self, p):
        self.buf.append(p)
        
    def draw(self, dc, f, **key):
        dc.SetPen(wx.Pen((0,255,255), width=1, style=wx.SOLID))
        if len(self.buf)>1:
            dc.DrawLines([f(*i) for i in self.buf])
        for i in self.buf:dc.DrawCircle(f(*i),2)
    
    def pop(self):
        a = self.buf
        self.buf = []
        return a
        
class Plugin(Tool):
    """FreeLinebuf class plugin with events callbacks"""
    def __init__(self):
        self.curobj = None
        self.doing = False
        self.helper = Linebuf()
        self.odx,self.ody = 0, 0
            
    def mouse_down(self, ips, x, y, btn, **key):
        lim = 5.0/key['canvas'].scale
        ips.mark = self.helper
        if btn==1:
            if not self.doing:
                if ips.roi!= None:
                    self.curobj = ips.roi.pick(x, y, ips.cur, lim)
                    ips.roi.info(ips, self.curobj)
                if self.curobj!=None:return
                    
                if ips.roi == None:
                    ips.roi = lineroi.LineRoi()
                    self.doing = True
                elif ips.roi.dtype=='line' and key['shift']:
                    self.doing = True
                else: ips.roi = None
            if self.doing:
                self.helper.addpoint((x,y))
                self.odx, self.ody = x,y
    
    def mouse_up(self, ips, x, y, btn, **key):
        if self.doing:
            self.doing = False
            self.curobj = None
            ips.roi.addline(self.helper.pop())
        ips.update()
    
    def mouse_move(self, ips, x, y, btn, **key):
        if ips.roi==None:return
        lim = 5.0/key['canvas'].scale       
        if btn==None:
            self.cursor = wx.CURSOR_CROSS
            if ips.roi.snap(x, y, ips.cur, lim)!=None:
                self.cursor = wx.CURSOR_HAND
        elif btn==1:
            if self.doing:
                self.helper.addpoint((x,y))
            elif self.curobj: ips.roi.draged(self.odx, self.ody, x, y, ips.cur, self.curobj)
            ips.update()
        self.odx, self.ody = x, y
        
    def mouse_wheel(self, ips, x, y, d, **key):
        pass