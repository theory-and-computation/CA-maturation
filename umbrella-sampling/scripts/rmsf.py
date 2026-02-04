#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import plotly.express as px


# To make the file we load here: we run the TCL script get-rmsf-linker-traj.tcl on the last 3 blocks of umbrella sampling:
# 

vmd -e calc-rmsf-linker-traj.tcl -args CA-umb/umb-122124/output/ coords_122124.txt
vmd -e calc-rmsf-linker-traj.tcl -args CA-umb/umb-010525/output/ coords_010525.txt
vmd -e calc-rmsf-linker-traj.tcl -args CA-umb/umb-012825/output/ coords_012825.txt

# Some processing is necessary on each file to get it in csv format:
sed "s/ /,/g" coords_122124.txt | sed "s/}\|{//g" > coords_CA_csv_last60.txt
sed "s/ /,/g" coords_010525.txt | sed "s/}\|{//g" >> coords_CA_csv_last60.txt
sed "s/ /,/g" coords_012825.txt | sed "s/}\|{//g" >> coords_CA_csv_last60.txt
# In[2]:


pmf = np.loadtxt("../wham-0512-last60/pmf.dat")

rows = np.unique(pmf[:,0]);
cols = np.unique(pmf[:,1]);

coords = np.loadtxt("../scripts/coords_CA_csv_last60.txt",delimiter=',')


# In[3]:


row_bins = [rows[np.argmin(np.abs(coords[i,0] - rows))] for i in range(coords.shape[0])]
col_bins = [cols[np.argmin(np.abs(coords[i,1] - cols))] for i in range(coords.shape[0])]


# In[4]:


coord_means = np.zeros((pmf.shape[0],coords.shape[1]))
coord_means[:,:2] = pmf[:,:2]

coord_count = np.zeros((len(rows), len(cols)))
coord_rmsf = np.zeros((len(rows), len(cols)))

for i in range(coord_means.shape[0]):
    id = np.where((row_bins == pmf[i,0]) * (col_bins == pmf[i,1]))
    if len(id[0])>0:
        coord_means[i,2:] = np.mean(coords[id[0],2:],axis=0)

        j = np.where(pmf[i,0]==rows);
        k = np.where(pmf[i,1]==cols);
        
        coord_count[j,k]=len(id[0])
        # decide here what residues will be considered
        coord_rmsf[j,k] = np.sqrt(np.mean((coords[id[0],2:] - coord_means[i,2:])**2))

#coord_means = coord_means[np.where(coord_means[:,-2]>0)[0]]


# In[5]:


fig = px.imshow(coord_count,aspect='auto',height=600,x=cols,y=rows)
fig.update_layout(    title={
        'text': "num. samples",
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    xaxis_title="ψ (Å)",
    yaxis_title="ϕ (°)",
    font=dict(size=20,family='Arial',color='black'),
    yaxis={'autorange':True})
fig.show()


# In[6]:


fig = px.imshow(coord_rmsf[7:-6,3:-2],aspect='square',height=600,x=cols[3:-2],y=rows[7:-6], \
               color_continuous_scale='Darkmint_r')
fig.update_layout(    title={
        'text': "RMSF",
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    xaxis_title="ψ (Å)",
    yaxis_title="φ (°)",
    font=dict(size=20,family='Arial',color='black'),
    yaxis={'autorange':True})
fig.show()
#fig.write_image('rmsf.svg')


# In[11]:


import pandas as pd
df = pd.DataFrame(columns=cols[3:-2],index=rows[7:-6],data=coord_rmsf[7:-6,3:-2])


# In[13]:


df.to_csv("../source data/rmsf.csv")


# In[ ]:




