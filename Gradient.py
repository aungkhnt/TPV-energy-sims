from TPVconfig import TPVconfig
from physics_utils import physics_utils
import numpy as np
from Irradiance import IrradianceModel

class GradientModel:
    def __init__(self, config: TPVconfig):
        self.cfg = config
        # self.temp = self.cfg.temp
        # self.d = self.cfg.d
        # self.width = self.cfg.width_e
        # self.height = self.cfg.height_e
        self.x_grid = self.cfg.x_grid
        self.y_grid = self.cfg.y_grid
        self.x_mesh, self.y_mesh = np.meshgrid(self.x_grid, self.y_grid)

        # self.dA_e = self.cfg.dA_e
        self.IrModel = IrradianceModel(config)
        self.irradiance_vect = np.vectorize(self.IrModel.calculate_Irradiance)

    def _calculate_gradient(self):

        z_matrix = self.irradiance_vect(self.x_mesh, self.y_mesh)
        gy , gx = np.gradient(z_matrix,self.cfg.dx, self.cfg.dy)
        self.gy = gy, self.gx = gx
        return gy, gx
    
    def _second_derivative(self):
        dxy , dxx = np.gradient(self.gx, self.y_mesh, self.x_mesh)

        dyy , _ = np.gradient(self.gy, self.y_mesh, self.x_mesh)
        self.dyy = dyy , self.dxx = dxx , self.dxy = dxy
        return dxx,dyy,dxy
    
    def find_hotspot(self):
        Hessian_det = (self.dxx * self.dyy) - (self.dxy**2)

        local_min = np.where(Hessian_det > 0 & self.dxx > 0 )
        local_max = np.where(Hessian_det > 0, self.dxx < 0)
        saddle_points = np.where(Hessian_det < 0 )
        return local_max
    

if __name__ == "__main__":
    import matplotlib as mpt 
    
        