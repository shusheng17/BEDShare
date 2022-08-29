#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
import warnings
from xml.dom.minidom import Element

warnings.simplefilter("ignore")
import hashlib
from pypbc import *
from gmpy2 import *
import time
import base64 as b64

 
def xor_encrypt(tips,key):
    ltips=len(tips)
    lkey=len(key)
    secret=[]
    num=0
    for each in tips:
        if num>=lkey:
            num=num%lkey
        secret.append( chr( ord(each)^ord(key[num]) ) )
        num+=1
 
    return b64.b64encode( "".join( secret ).encode() ).decode()
 
 
def xor_decrypt(secret,key):
 
    tips = b64.b64decode( secret.encode() ).decode()
 
    ltips=len(tips)
    lkey=len(key)
    secret=[]
    num=0
    for each in tips:
        if num>=lkey:
            num=num%lkey
 
        secret.append( chr( ord(each)^ord(key[num]) ) )
        num+=1
 
    return "".join( secret )


class Node():
    """节点，保存数据和后继节点"""
    def __init__(self, elem):
        self.elem = elem
        self.next = None

class Linklist():
    def __init__(self, node=None):
        self.__head = node
    def add(self, item):
        """在链表头部添加"""
        node = Node(item)

        node.next = self.__head
        self.__head = node
    def travel(self, t):
        """遍历链表"""
        cur = self.__head
        l = []

        while cur != None:
            # print(cur.elem)
            l.append(cur.elem)
            cur = cur.next
        return l


def Setup():
    q_1 = get_random_prime(60)
    q_2 = get_random_prime(60)
    q = q_1*q_2
    params = Parameters( n = q_1 * q_2 )   
    pairing = Pairing( params )
    H = hashlib.sha256

    h1 = lambda w: Element.from_hash(pairing,Zr,H(str(w).encode('utf-8')).hexdigest())
    h2 = lambda w: H(str(w).encode('utf-8'))
    g = Element.random(pairing, G1) 

    para = (q, g, h1, h2, pairing)
    return para


def KeyGen(para):
    pairing = para[4]
    b = Element.random(pairing,Zr)
    return b


def Update(para,w,cid,edb):
    _,g,h1,h2,pairing = para

    rw = Element.random(pairing,Zr)
    vw = Element(pairing,G1,value = g**rw)
    tw = Element(pairing,G1,value = vw**h1(w))

    keyw = h2(tw).hexdigest()
    # print(keyw.hexdigest())
    # keyw = str(tw)
    # print(str(keyw))
    if (keyw not in edb):
        ll = Linklist()
    else:
        ll = edb[keyw]

    valw = xor_encrypt(cid,str(tw))
    ll.add(valw)
    # ll.add(xor_encrypt("cid",str(tw)))

    edb[keyw] = ll

    return edb, rw


def DataAut(para, b, rw):
    q,g,_,_,pairing = para
    d = invert(mpz(b), mpz(q)) #d为b的逆元
    req_w = Element(pairing,G1,value = g**int(d))
    aut_du_w = req_w**rw
    return aut_du_w


def Trapdoor(para, aut_du_w, b, w):
    _,_,h1,_,pairing = para
    # Tw = (aut_du_w**b)**h1(w) #和下面的等价
    Tw = Element(pairing,G1,value = (aut_du_w**h1(w))**b)
    return Tw


def Search(edb, keyw, Tw):
    ll = edb[keyw]
    cids = ll.travel(str(Tw))
    # cid = xor_decrypt(edb[keyw],str(Tw))
    # print(cids)
    cids = [xor_decrypt(i,str(Tw)) for i in cids]
    # print(cids)
    return cids
