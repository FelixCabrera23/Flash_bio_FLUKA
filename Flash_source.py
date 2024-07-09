#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 11:14:40 2024

@author: Felix Cabrera

THIS SCRIPT IS MENT TO BE USED ONLY WITH DATA FROM THE ADECUATE SOURCE AND MAY
NOT WORK IF USED WITH DIFFERENT FORMAT DATA.

Analisis and plots of flash simulation from FLUKA

"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d


def read_data_file (file_path):
    """
    This func taces the file path of the data from the FLUKA simulation and 
    returns it into a matrix form
    
    ignores commented lines that beggin with '#'
    
    works with FLUKA 
    """ 
    data_temp = []
    with open(file_path, 'r') as file:
        for line in file:
            data_temp.append(line.strip())
    
    Dat_mat = []

    for line in data_temp:
        list_temp = line.split()
        if list_temp[0] != '#':        
            float_temp = [float(string) for string in list_temp]
            Dat_mat.append(float_temp)
        
    return(Dat_mat)

def Data_simulated (Data_matrix,norm=False, scale =10, norm_val = 1):
    """
    This function takes the data matrix from FLUKA 
    and returns list of the radious, dose, and error data
    
    the 'scale' changes the scale of the data in the x coordinate
    the 'norme' normalizes the measurment result to 'norm_val'

    """
  
    x1_tmp,x2_tmp,meas_tmp,error_tmp = [],[],[],[]

    for line in Data_matrix:
        x1_tmp.append(line[0]*scale)
        x2_tmp.append(line[1]*scale)
        meas_tmp.append(line[2])
        error_tmp.append(line[3])
        
    if norm: meas_tmp = normalize(meas_tmp, norm_Val=norm_val)
        
    return(x1_tmp,x2_tmp,meas_tmp,error_tmp)

def normalize (list_temp,norm_Val = 1):
    """
    Esta funcion normaliza una lista a 1
    """
    norm_list = []
    max_list = max(list_temp)/norm_Val
    for i in list_temp: 
        norm_list.append(i/max_list)


def Energy_spectra_plot (file_path = 'Sample_data/Energy_flux_before.lis', x_log = False, y_log = False ,norm = True):
    """
    This func plots the energy spectrum provided the data from a FLUKA '.lis' file
    with adecuate format

    Parameters
    ----------
    file_path : flie path to the flux data
        DESCRIPTION. The default is 'Sample_data/Energy_flux_before.lis'.
    x_log : boolean sets logarithmic scale on x axis
    y_log : boolean sets logarithmic scale on y axis
    norm : boolean sets the

    """
    data_flux = read_data_file(file_path)
    E1,E2,Flx,Flx_err = Data_simulated(data_flux, norm=norm,scale=1000)
    
    if x_log:
        plt.xscale('log')
        
    if y_log:
        plt.yscale('log')
        
    plt.plot(E1,Flx)
    plt.xlabel(r"MeV")
    plt.ylabel(r"Photon fluence")
    plt.show()
    
    def PDD_plot (file_path = 'Sample_data/Coll_60mm_PDD.dat',norm=True):
        
        
        pdd_data = read_data_file(file_path)
        
        Z1, Z2, Dose, Dose_err = Data_simulated(pdd_data,norm=norm,scale=10)
        
        plt.plot(Z1,Dose)
        plt.xlabel(r'Distance [mm]')
        plt.ylabel(r'Normalized Dose')
        plt.show()
        
############## TEST AREA ############

test_data100 = read_data_file('OXIGEN100/PDD.dat')
test_data150 = read_data_file('OXIGEN150/PDD.dat')
test_data000 = read_data_file('OXIGEN000/PDD.dat')

test_data100_w = Data_simulated(test_data100)
test_data150_w = Data_simulated(test_data150)
test_data000_w = Data_simulated(test_data000)

x100,x100m,y100,y100err = [list(data) for data in test_data100_w]
x150,x150m,y150,y150err = [list(data) for data in test_data150_w]
x000,x000m,y000,y000err = [list(data) for data in test_data000_w]

plt.plot(x100,y100,label='100')
plt.plot(x000,y000,label='000')
plt.legend()
plt.show()

















