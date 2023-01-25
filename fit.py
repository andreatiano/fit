#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 18:52:30 2023

@author: andreatiano
"""

from scipy.interpolate import interp1d
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(layout="wide")
plotCol, dataCol = st.columns([2,1])

importExp=st.sidebar.expander('Import Option')
fileName = importExp.file_uploader("Import spectra",accept_multiple_files=False)
delimiter= importExp.selectbox('Delimiter:',('\t',';',','))
if fileName is not None:
    arr = np.loadtxt(fileName,delimiter=delimiter,skiprows=1)

    x=arr[:,0]
    xless=np.arange(190,np.min(arr[:,0]),5)
    x=int(x)
    xless=int(xless)
    n=arr[:,1]
    k=arr[:,2]
    k2 = [0 for i in range(8)]
    n2 = [0 for i in range(8)]

    xfull = np.concatenate((xless,x),axis=0)
    k = np.concatenate((k2,k),axis=0)
    n= np.concatenate((n2,n),axis=0)
    xnew=np.arange(np.min(xfull),np.max(arr[:,0])+1,1)

    nfit=interp1d(xfull, n, kind='cubic')
    kfit=interp1d(xfull, k, kind='cubic')

    fig=plt.figure(1)
    plt.plot(xfull, n, '.', xfull, k, '.', xfull, nfit(xfull), '-',xfull, kfit (xfull), '-')
    plt.legend(['n_data','k_data', 'n_fit', 'k_fit'], loc='best')
    st.pyplot(fig)

    plotData=dataCol.expander('fitted data',True)
    plotDataFrame=pd.DataFrame(np.vstack((xfull,nfit(xfull),kfit(xfull))).transpose(),columns = ['wavelenght','n','k'])
    plotData.dataframe(plotDataFrame) 
    plotData.download_button('Download current spectra data',plotDataFrame.to_csv().encode('utf-8'),'fittedspectra.txt')