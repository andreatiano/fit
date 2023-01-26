from scipy.interpolate import interp1d
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(layout="wide")
plotCol, dataCol = st.columns([2,1])


importExp=st.sidebar.expander('Import Option')
skip=importExp.checkbox("First row is a string")
fileName = importExp.file_uploader("Import spectra",accept_multiple_files=False)
delimiter= importExp.selectbox('Delimiter:',('\t',';',','))



if fileName is not None:
    row=0
    if skip is True:
        row=1
    arr = np.loadtxt(fileName,delimiter=delimiter,skiprows=row)
    x=arr[:,0]
    step=x[1]-x[0]
    firsWave=st.insert_number("Insert the first wavelenght of the spectra", min_value=100, max_value=np.min(arr[:,0], step=step, value=np.min(arr[:,0])
    xless=np.arange(firsWave,np.min(arr[:,0]),step)
    n=arr[:,1]
    k=arr[:,2]
    k2 = [0 for i in range(int((np.min(x)-firsWave)/step))]
    n2 = [0 for i in range(int((np.min(x)-firsWave)/step))]

    xfull = np.concatenate((xless,x),axis=0)
    k = np.concatenate((k2,k),axis=0)
    n= np.concatenate((n2,n),axis=0)
    xnew=np.arange(np.min(xfull),np.max(arr[:,0])+1,1)

    nfit=interp1d(xfull, n, kind='cubic')
    kfit=interp1d(xfull, k, kind='cubic')
    
    specraPlot=plotCol.expander('Dispersion curves')
    fig=plt.figure(1)
    plt.plot(xfull, n, '.', xfull, k, '.', xnew, nfit(xnew), '-',xnew, kfit (xnew), '-')
    plt.legend(['n_data','k_data', 'n_fit', 'k_fit'], loc='best')
    specraPlot.pyplot(fig)

    plotData=dataCol.expander('fitted data',True)
    plotDataFrame=pd.DataFrame(np.vstack((xnew,nfit(xnew),kfit(xnew))).transpose(),columns = ['wavelenght','n','k'])
    plotData.dataframe(plotDataFrame) 
    plotData.download_button('Download current spectra data',plotDataFrame.to_csv().encode('utf-8'),'fittedspectra.txt')