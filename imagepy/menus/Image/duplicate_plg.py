# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 19:47:34 2016
@author: yxl
"""

from imagepy.core.engine import Simple
from imagepy.core import ImagePlus
from imagepy.core.manager import ImageManager
import numpy as np
from imagepy import IPy

class Duplicate(Simple):
    title = 'Duplicate'
    note = ['all']
    
    para = {'name':'Undefined','stack':True}
    
    def load(self, ips):
        self.para['name'] = ips.title+'-copy'
        self.view = [(str, 'name', 'Name', '')]
        if ips.get_nslices()>1:
            self.view.append((bool, 'stack', 'duplicate stack'))
        return True
    #process
    def run(self, ips, imgs, para = None):
        name = para['name']
        print('name------------------', name)
        if ips.get_nslices()==1 or self.para['stack']==False:
            if ips.roi == None:
                img = ips.img.copy()
                ipsd = ImagePlus([img], name)
                ipsd.back = ips.back
            else:
                img = ips.get_subimg().copy()
                ipsd = ImagePlus([img], name)
                box = ips.roi.get_box()
                ipsd.roi = ips.roi.affine(np.eye(2), (-box[0], -box[1]))
                '''
                if not ips.backimg is None:
                    sr, sc = ips.get_rect()
                    ipsd.backimg = ips.backimg[sr, sc]
                '''
        elif ips.get_nslices()>1 and self.para['stack']:
            if ips.roi == None:
                if ips.is3d:imgs=imgs.copy()
                else:imgs = [i.copy() for i in imgs]
                #backimg = ips.backimg
            else:
                sc, sr = ips.get_rect()
                if ips.is3d: imgs=imgs[:, sc, sr].copy()
                else: imgs = [i[sc,sr].copy() for i in imgs]
                #if not ips.backimg is None:
                #    backimg = None #ips.backimg[sr, sr]
            ipsd = ImagePlus(imgs, name)
            if ips.roi != None:
                ipsd.roi = ips.roi.affine(np.eye(2), (-sr.start, -sc.start))
            #if not ips.backimg is None: ipsd.backimg = backimg
        ipsd.chan_mode = ips.chan_mode
        IPy.show_ips(ipsd)

class Rename(Simple):
    title = 'Rename'
    note = ['all']
    
    para = {'name':'Undefined'}
    view = [(str, 'name', 'name', '')]
    #process
    def run(self, ips, imgs, para = None):
        ips.title = ImageManager.name(para['name'])

plgs = [Rename, Duplicate]