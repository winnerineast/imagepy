# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 17:35:09 2016

@author: yxl
"""
import wx
from imagepy.core.engine import Tool
import numpy as np
from imagepy.core.manager import ColorManager
from skimage.morphology import flood_fill, flood
from skimage.measure import find_contours
from imagepy.core.roi.convert import shape2roi, roi2shape
from shapely.geometry import Polygon, Point
from shapely.ops import cascaded_union
import matplotlib.pyplot as plt

def polygonize(conts, withholes = False):
    for i in conts:i[:,[0,1]] = i[:,[1,0]]
    polygon = Polygon(conts[0]).buffer(0)
    if not withholes:return polygon
    holes = []
    for i in conts[1:]:
        if len(i)<4:continue
        holes.append(Polygon(i).buffer(0))
    hole = cascaded_union(holes)
    return polygon.difference(hole)

   
class Plugin(Tool):
    title = 'Magic Stick'
    para = {'tor':10, 'con':'8-connect'}
    view = [(int, 'tor', (0,1000), 0, 'torlorance', 'value'),
            (list, 'con', ['4-connect', '8-connect'], str, 'fill', 'pix')]

    def __init__(self):
        self.curobj = None
        self.oper = ''
            
    def mouse_down(self, ips, x, y, btn, **key): 
        lim = 5.0/key['canvas'].scale 
        if btn==1 or btn==3:
            if ips.roi!= None:
                self.curobj = ips.roi.pick(x, y, ips.cur, lim)
                ips.roi.info(ips, self.curobj)
            if not self.curobj in (None,True):return
            if ips.roi == None:
                connectivity=(self.para['con']=='8-connect')+1
                img = ips.img.reshape((ips.img.shape+(1,))[:3])
                msk = np.ones(img.shape[:2], dtype=np.bool)
                for i in range(img.shape[2]):
                    msk &= flood(img[:,:,i], (int(y),int(x)), 
                        connectivity=connectivity, tolerance=self.para['tor'])
                conts = find_contours(msk, 0, 'high')
                ips.roi = shape2roi(polygonize(conts, btn==3))
            elif hasattr(ips.roi, 'topolygon'):
                shp = roi2shape(ips.roi.topolygon())
                oper = ''
                if key['shift']: oper = '+'
                elif key['ctrl']: oper = '-'
                elif self.curobj: return
                else: ips.roi=None

                connectivity=(self.para['con']=='8-connect')+1
                img = ips.img.reshape((ips.img.shape+(1,))[:3])
                msk = np.ones(img.shape[:2], dtype=np.bool)
                for i in range(img.shape[2]):
                    msk &= flood(img[:,:,i], (int(y),int(x)), 
                        connectivity=connectivity, tolerance=self.para['tor'])
                conts = find_contours(msk, 0, 'high')
                cur = polygonize(conts, btn==3)
                if oper == '+':
                    ips.roi = shape2roi(shp.union(cur))
                elif oper == '-':
                    ips.roi = shape2roi(shp.difference(cur))
                else: ips.roi = shape2roi(cur)

            else: ips.roi = None

        ips.update()
        
    def mouse_up(self, ips, x, y, btn, **key):
        ips.update()
    
    def mouse_move(self, ips, x, y, btn, **key):
        if ips.roi==None:return
        lim = 5.0/key['canvas'].scale
        if btn==None:
            self.cursor = wx.CURSOR_CROSS
            if ips.roi.snap(x, y, ips.cur, lim)!=None:
                self.cursor = wx.CURSOR_HAND
        elif btn==1:
            if self.curobj: ips.roi.draged(self.odx, self.ody, x, y, ips.cur, self.curobj)
            ips.update()
        self.odx, self.ody = x, y
        
    def mouse_wheel(self, ips, x, y, d, **key):
        pass