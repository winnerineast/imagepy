# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 11:26:12 2016
@author: yxl
"""
from imagepy.core.engine import Simple
from imagepy import IPy

class SetSlice(Simple):
    title = 'Set Slice'
    note = ['all']
    
    #parameter
    para = {'num':0}
    view = [(int, 'num', (0,999), 0, 'Num', '')]

    #process
    def run(self, ips, imgs, para = None):
        if para['num']>=0 and para['num']<ips.get_nslices():
            ips.set_cur(para['num'])
        
class Next(Simple):
    title = 'Next Slice'
    note = ['all']

    #process
    def run(self, ips, imgs, para = None):
        if ips.cur<ips.get_nslices()-1:
            ips.cur+=1
            
class Pre(Simple):
    title = 'Previous Slice'
    note = ['all']

    #process
    def run(self, ips, imgs, para = None):
        if ips.cur>0:
            ips.cur-=1
            
class Delete(Simple):
    title = 'Delete Slice'
    note = ['stack', 'all']

    #process
    def run(self, ips, imgs, para = None):
        ips.imgs.pop(ips.cur)
        if ips.cur==ips.get_nslices():
            ips.cur -= 1
            
class Add(Simple):
    title = 'Add Slice'
    note = ['all']

    #process
    def run(self, ips, imgs, para = None):
        ips.imgs.insert(ips.cur, ips.img*0)
            
class Sub(Simple):
    title = 'Sub Stack'
    modal = False
    note = ['all']

    para = {'start':0, 'end':10}
    view = [(int, 'start', (0,1e8), 0, 'start', 'slice'),
            (int, 'end', (0,1e8), 0, 'end', 'slice')]

    def run(self, ips, imgs, para = None):
        (sc, sr), sz = ips.get_rect(), slice(para['start'], para['end'])
        if ips.is3d: imgs = imgs[sz, sc, sr].copy()
        else: imgs = [i[sc,sr].copy() for i in imgs[sz]]
        IPy.show_img(imgs, ips.title+'-substack')

plgs = [SetSlice, Next, Pre, Add, Delete, '-', Sub]