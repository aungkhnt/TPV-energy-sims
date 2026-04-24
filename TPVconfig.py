from dataclasses import dataclass
import numpy as np
@dataclass

class TPVconfig:
    """The configuration file where all universal constants and reusable equations go"""
    
    # ======================================================================
    ## constants
    sigma:float = 5.670373e-8 # Stefan-Boltzmann Constant
    wienConstant:float = 2898 # 2898 mK
    h_planck:float = 6.62607015e-34 # Joule second - planck's constant
    c_light:float = 2.998e8 # meter per second - speed of light
    k_boltz:float = 1.38e-23 # boltzmann constant for spectral distribution shape 
    lambda_min: float = 100e-9
    lambda_max: float = 5e-6

    MATERIALS = {
    "silicon" : {"Eg": 1.12, "eps_high":0.9, "eps_low":0.5},
    "germanium": {"Eg":0.66 , "eps_high":0.85 , "eps_low":0.1},
    "blackbody": {"Eg": 0.0, "eps_high":1.0, "eps_low":1.0}
    }
    # ======================================================================
    
    # ======================================================================
    # Inputs
    material_name: str 
    temp: float # Temperature of emitter/heat source
    # parameters of emitter & cell
    d: float # gap distance between cell and emitter
    width_e: float  # width of emitter
    height_e: float # height of emitter
    # x: float # x-coord
    # y: float # y-coord of the cell
    x_e: float # x-coord
    y_e: float # y-coord of emitter

    xnum: int = 50 
    ynum: int = 50
    # ======================================================================

    # ======================================================================
    # derived values
    def __post_init__(self):
        self.x_grid: int = np.linspace(-self.width_e/2,self.width_e/2, self.xnum)
        self.y_grid: int = np.linspace(-self.height_e/2, self.height_e/2, self.ynum)
        self.dx: float = self.width_e/self.xnum
        self.dy: float = self.height_e/self.ynum
        self.dA_e: float = self.dx* self.dy

    # ======================================================================
