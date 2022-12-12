from fury3D import CreateScene, CreateSnapshots
from pyMCDS import pyMCDS
from pathlib import Path
import numpy as np
import pandas as pd
import sys

def my_custom_coloring_function(df_cells):
    Gene_RFP = np.array([df_cells['genes_x']])
    RFP = np.where(Gene_RFP == 1)
    GFP = np.where(Gene_RFP == 0)
    # Colors
    Colors = np.ones((len(df_cells),4)) # 4 channels RGBO
    # RFP+ cells - Red
    Colors[RFP[1],0] = 1
    Colors[RFP[1],1] = 0
    Colors[RFP[1],2] = 0
    # GFP+ cells - Green
    Colors[GFP[1],0]= 0
    Colors[GFP[1],1] = 1
    Colors[GFP[1],2] = 0
    Colors_nucleus = Colors.copy()
    return Colors, Colors_nucleus

def coloring_function_KI67_stain(df_cells):
    Cell_phase = np.array([df_cells['current_phase']])
    Gene_RFP = np.array([df_cells['genes_x']])
    Ki67p = np.where(Cell_phase == 2)
    Ki67n = np.where(Cell_phase != 2)
    RFP = np.where(Gene_RFP == 1)
    GFP = np.where(Gene_RFP == 0)
    # Colors
    Colors = np.ones((len(df_cells),4)) # 4 channels RGBO
    Colors_nucleus = np.ones((len(df_cells),4)) # 4 channels RGBO
    # Ki67+ cells - Nucleus white
    Colors_nucleus[Ki67p[1],0] = 1
    Colors_nucleus[Ki67p[1],1] = 1
    Colors_nucleus[Ki67p[1],2] = 1
    # Ki67- cells - Nucleus black
    Colors_nucleus[Ki67n[1],0] = 0
    Colors_nucleus[Ki67n[1],1] = 0
    Colors_nucleus[Ki67n[1],2] = 0
    # RFP+ cells - Cytoplasm red
    Colors[RFP[1],0] = 1
    Colors[RFP[1],1] = 0
    Colors[RFP[1],2] = 0
    # GFP+ cells - Cytoplasm green
    Colors[GFP[1],0]= 0
    Colors[GFP[1],1] = 1
    Colors[GFP[1],2] = 0
    return Colors, Colors_nucleus

def my_custom_header_function(mcds):
    # Current time
    curr_time = round(mcds.get_time(),2) # min
    time_days = curr_time//1440.0
    time_hours = (curr_time%1440.0)//60
    time_min = ((curr_time%1440.0)%60)
    # Selecting RFP+ and GFP+ cells
    Gene_RFP = np.array([mcds.data['discrete_cells']['genes_x']])
    RFP = np.where(Gene_RFP == 1)
    GFP = np.where(Gene_RFP == 0)
    Count_RFP = len(RFP[1])
    Count_GFP = len(GFP[1])
    title_text = "Current time: %02d days, %02d hours, and %0.2f minutes \n\n RFP+: %d agents and GFP+: %d agents"%(time_days,time_hours,time_min,Count_RFP,Count_GFP)
    return title_text

if __name__ == '__main__':
    if (len(sys.argv) != 3 and len(sys.argv) != 2):
      print("Please provide\n 1 arg [folder]: to taking snapshots from the folder \n or provide 2 args [folder] [frame ID]: to interact with scene!")
      sys.exit(1)
    if (len(sys.argv) == 3):
      # AddBox = {'xmin': 600, 'xmax': 800, 'ymin': -370, 'ymax': -170, 'zmin': 150, 'zmax': 350} # output00 (200 microns^3)
      AddBox = {'xmin': -70, 'xmax': 280, 'ymin': 650, 'ymax': 1000, 'zmin': 320, 'zmax': 670} # output01 (350 microns^3)
      # CreateScene(Path(sys.argv[1]),"output%08d.xml"%int(sys.argv[2]), coloring_function=my_custom_coloring_function, header_function=my_custom_header_function, AddBox = AddBox)
      # CreateScene(Path(sys.argv[1]),"output%08d.xml"%int(sys.argv[2]), coloring_function=coloring_function_KI67_stain, header_function=my_custom_header_function, BoxCrop = AddBox, PlotNucleus=True)
      # SNAPSHOTS
      # CreateSnapshots(Path(sys.argv[1]),file="output%08d.xml"%int(sys.argv[2]), coloring_function=my_custom_coloring_function, header_function=my_custom_header_function,size_window=(5000,5000), PlotNucleus=True, AddBox = AddBox)
      # CreateSnapshots(Path(sys.argv[1]),file="output%08d.xml"%int(sys.argv[2]), coloring_function=my_custom_coloring_function, header_function=my_custom_header_function,size_window=(5000,5000), PlotNucleus=True, BoxCrop = AddBox)
      # CreateSnapshots(Path(sys.argv[1]),file="output%08d.xml"%int(sys.argv[2]), coloring_function=coloring_function_KI67_stain, header_function=my_custom_header_function,size_window=(5000,5000), PlotNucleus=True, AddBox = AddBox)
      CreateSnapshots(Path(sys.argv[1]),file="output%08d.xml"%int(sys.argv[2]), coloring_function=coloring_function_KI67_stain, header_function=my_custom_header_function,size_window=(5000,5000), PlotNucleus=True, BoxCrop = AddBox)
    if (len(sys.argv) == 2):
      CreateSnapshots(Path(sys.argv[1]), coloring_function=my_custom_coloring_function, header_function=my_custom_header_function, PlotNucleus=True)
