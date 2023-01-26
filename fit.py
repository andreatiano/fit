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
st.sidebar.title(':blue[Dispersion fitting] :sunglasses:')

importExp=st.sidebar.expander('Import Option')
skip=importExp.checkbox("First row is a string")
fileName = importExp.file_uploader("Import dispersion",accept_multiple_files=False)
delimiter= importExp.selectbox('Delimiter:',('\t',';',','))



if fileName is not None:
    row=0
    if skip is True:
        row=1
    arr = np.loadtxt(fileName,delimiter=delimiter,skiprows=row)
    x=arr[:,0]
    xmin=np.min(arr[:,0])
    step=x[1]-x[0]
    firstWave=plotCol.number_input("Insert the first wavelenght of the spectra", min_value=float(100), max_value= xmin, step=step, value= xmin)
    xfull=x
    n=arr[:,1]
    nmin=arr[0,1]
    k=arr[:,2]
    kmin=arr[0,2]
    
    if firstWave< xmin:                                                                  
        xless=np.arange(firstWave, xmin,step)
        xfull = np.concatenate((xless,x),axis=0)
        k2 = [kmin for i in range(int(( xmin-firstWave)/step))]
        n2 = [nmin for i in range(int(( xmin-firstWave)/step))]
        k = np.concatenate((k2,k),axis=0)
        n= np.concatenate((n2,n),axis=0)
        
    xnew=np.arange(np.min(xfull),np.max(arr[:,0])+1,1)

    nfit=interp1d(xfull, n, kind='cubic')
    kfit=interp1d(xfull, k, kind='cubic')
    
    specraPlot=plotCol.expander('Dispersion curves',True)
    fig=plt.figure(1)
    plt.plot(xfull, n, '.', xfull, k, '.', xnew, nfit(xnew), '-',xnew, kfit (xnew), '-')
    plt.legend(['n_data','k_data', 'n_fit', 'k_fit'], loc='best')
    plt.xlabel("Wavelenght [nm]")
    plt.ylabel("n,k")
    specraPlot.pyplot(fig)

    plotData=dataCol.expander('fitted data',True)
    plotDataFrame=pd.DataFrame(np.vstack((xnew,nfit(xnew),kfit(xnew))).transpose(),columns = ['wavelenght','n','k'])
    plotData.dataframe(plotDataFrame) 
    plotData.download_button('Download current spectra data',plotDataFrame.to_csv(header=False,index=False,sep ='\t').encode('utf-8'),'fittedspectra.txt')
