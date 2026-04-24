'''
Irradiance ∝ 1/r^4
Energy Conversion Chain: Heat source -> Emitter(radiation) -> TPV cell
Irradiance = how many watts per square meter are hitting each specific spot
TPV converts I(x,y) into J(current density) and V(voltage)

Difference between PV vs TPV - for PV emitter is far and irradiance is the same. TPV, emitter is close and irradiance is different at different (x,y).
'''

import numpy as np
import matplotlib as mpt
from planckSpectrumModel import stefboltz
from TPVconfig import TPVconfig
from physics_utils import physics_utils
# =============================================================
# =============================================================
# 

class IrradianceModel:

    def __init__(self, config: TPVconfig):
        self.cfg = config
        self.temp = self.config.temp
        self.x_e = self.cfg.x_e
        self.y_e = self.cfg.y_e
        self.d = self.cfg.d
        self.width = self.cfg.width_e
        self.height = self.cfg.height_e
        self.x_grid = self.cfg.x_grid
        self.y_grid = self.cfg.y_grid
        self.dA_e = self.cfg.dA_e

    def _point_2_point_contribution(self, x,y, xe, ye):
        L = physics_utils.steradianPower(self.temp)

        r_squared = (x - xe)**2 + (y- ye)**2 + self.d**2

        return (L * self.d**2) / (r_squared**2)
    
    def _use_point_source(self):
        return max(self.width, self.height) < (0.1*self.d)
    
    def calculate_Irradiance(self,x= 0,y=0):
        if self._use_point_source():
            A_total = self.width * self.height
            return self._point_2_point_contribution(x,y,0,0) * A_total
        
        xe_mesh, ye_mesh = np.meshgrid(self.x_grid,self.y_grid)
        all_contributions = self._point_2_point_contribution(x,y,xe_mesh, ye_mesh)

        return np.sum(all_contributions) * self.dA_e
        


 
# # =============================================================
# # irradiance at any arbitrary(x,y) 
# # taking the emitter as one dot(uniform radiation)
# def Irradiance(temp:float, d,x,x_e,y,y_e, width_e, height_e: float, theta1, theta2, xnum =50,  ynum = 50):
#     L = steradianPower(temp)

    
#     r_squared = (x-x_e)**2 + (y-y_e)**2 + d**2
#     A_e = width_e * height_e

#     dx = width_e/xnum
#     dy = height_e/ynum
#     dA_e = dx * dy

#     x_grid = np.linspace(-width_e/2, width_e/2, xnum)
#     y_grid = np.linspace(-height_e/2, height_e/2, ynum)

#     """
#     Common case: Point-source approximation
#     """
#     if use_point_source(width_e, height_e, d):
#         return point_2_point_contribution(temp,x,y,d) * A_e

#     """
#     Double integral for every emitter's x_e,y_e patch's radiation onto cell's (x,y) patch
#     """
#     I_total = 0.0
#     for x_e in x_grid:
#         for y_e in y_grid:
#             I_total += point_2_point_contribution(temp,x,x_e,y,y_e,d) * dA_e
#     return I_total
