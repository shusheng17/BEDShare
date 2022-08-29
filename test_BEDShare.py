from BEDShare import *

 # Setup
para = Setup()
q,g,h1,h2,pairing = para


# KeyGen
kdu = KeyGen(para)


w = 'keyword'
cid = '123457890'
edb=dict()


# Update
start_time = time.time()
edb, rw = Update(para,w,cid,edb)
time_cost = time.time() - start_time
print('Update cost',time_cost)


# DataAut
start_time = time.time()
aut_du_w = DataAut(para, kdu, rw)
time_cost = time.time() - start_time
print('DataAut cost',time_cost)


# Trapdoor
start_time = time.time()
Tw = Trapdoor(para, aut_du_w, kdu, w)
time_cost = time.time() - start_time
print('Trapdoor cost',time_cost)


# Search
start_time = time.time()
cids = Search(edb, h2(Tw).hexdigest(), Tw)
# print('se2arch results:',cids)
time_cost = time.time() - start_time
print('Search cost',time_cost)
