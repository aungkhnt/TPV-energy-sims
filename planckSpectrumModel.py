'''
Name : planckSpectrumM1-1.py
Description: planck Spectrum Equation Module 1, submodule 1
Type : Support Function 
Question : "How much radiation does the emitter produce, and at what wavelengths?"
'''

""
import numpy as np
import matplotlib as mpt
import TPVconfig
import physics_utils
# ##################################################################################
# # Defining Constants in advance




# # 1. Stefan-Boltzmann Law

# def stefBoltz(temp_k, emissivity = 1.0):
#     """
#     Calculates radiant exitance,aka, total radiant heat energy of a uniformly radiant black body as well as non-black body in W/m^2.
#     default emissivity (if black body) = 1.0
#     """

#     # Equation : E = epsilon * sigma * T^4
#     radiant_exitance = emissivity * sigma * (temp_k**4)
#     return radiant_exitance

# # 2. Wien's Displacement Law
# def WienDisp(temp_k = None, peakLambda = None):
#     """
#     shows inverse proportionality between Temp of an object and wavelength of light it emits most intensely
#     """
#     if temp_k is not None:
#         return wienConstant/temp_k
    
#     elif peakLambda is not None:
#         return wienConstant/peakLambda

#     else:
#         return "Please provide either temp_k or peakLambda."
    

# ## Edge Case Handling   
# # 3. Selective Emitter
# def selectiveEmit(energyBandGap, Lambda, eps_high = 0.9, eps_low =0.05):
    
#     lambdaBandGap = (h_planck*c_light)/energyBandGap

#      # Bandgap Energy differs per material
#     # to be further developed using transparency-total blackbody spectrum, thermal equilibrium, and urbach tail absorption coefficient
#     return np.where(Lambda<=lambdaBandGap, eps_high, eps_low )

# # 4. Planck's spectral radiance 

# def totalPower(Lambda, temp_k, material_name="blackbody"):

#     materialProp = MATERIALS.get(material_name.lower(),MATERIALS["blackbody"])
#     energyBandGap = materialProp["Eg"]*1.60218e-19

#     C1 = (2 * h_planck * (c_light**2) ) / (Lambda**5) # first constant 2hc^2/lambda^5
#     phoE = (h_planck * c_light) / Lambda # Photon Energy E = hf, f = c/lambda
#     thermE = k_boltz * temp_k # thermal energy = kT

#     with np.errstate(over = 'ignore'):
#         boltzFactor = np.exp(phoE/thermE) #Planck distribution factor. It’s what gives the blackbody curve its distinct "hill" shape.
    
#         planckSpectral = C1*(1/(boltzFactor -1))


#     emissivity = selectiveEmit(energyBandGap, Lambda, materialProp["eps_high"], materialProp["eps_low"]) # Lambda is a vector or a np array
    
#     radiance = planckSpectral * emissivity

#     return np.trapezoid(radiance,Lambda) 



'''
Output Testing
wavelengths = np.linspace(400e-9, 500e-12, 50)
temp_k = np.linspace(2500, 4000, 50)
radiance = planckSpectral(wavelengths, temp_k)

#print (radiance[:10])'''

# ====================================================================
## Using OOP and Classes
# ====================================================================

class PlanckModel:

    def __init__(self, config: TPVconfig):
        self.cfg = config
        m_name = self.cfg.material_name.lower()
        self.mat = self.MATERIALS.get(m_name, self.MATERIALS["blackbody"])
        self.h = self.cfg.h_planck
        self.c = self.cfg.c_light
        self.k = self.cfg.k_boltz
        self.temp = self.cfg.temp


    
    def _selective_emit(self, Lambda):
        Eg = self.mat["Eg"]
        Eg_bg = Eg * (1.602e-19)
        eps_low = self.mat["eps_low"]
        eps_high = self.mat["eps_high"]

        lambda_bg = (self.h_planck * self.c_light) / Eg_bg

        return np.where(Lambda <= lambda_bg, eps_high, eps_low)
    
    def _calculate_spectral_radiance(self, Lambda: np.ndarray) -> np.ndarray:
        """Returns the y-value of the planck curve with Lambda array values being x values"""
        C1 = ( 2 * self.h * (self.c**2)) / (Lambda**5)
        pE = ( self.h * self.c) / Lambda 
        tE = self.k * self.temp 

        with np.errstate( over = 'ignore'):
            boltzFactor = np.exp(pE/tE)
            planck_raw = C1*(1/(boltzFactor-1))

        emissivity = self._selective_emit(Lambda)

        return planck_raw * emissivity  # this will return an array of radiance values

    def get_total_power(self, Lambda_range: np.ndarray) -> float: 
        
        radiance = self._calculate_spectral_radiance(Lambda_range)

        return np.trapezoid(radiance, Lambda_range)


# =================================================================
# Guard 

if __name__ == "__main__":

    cfg = TPVconfig(temp=2500, material_name = "germanium")

    model = PlanckModel(cfg)

    lambdas = np.linspace(cfg.lambda_min, cfg.lambda_max, 500)
    curve = model._calculate_spectral_radiance(lambdas)
    total_W = model.get_total_power(lambdas)

    import matplotlib.pyplot as plt
    plt.plot(lambdas,curve)
    plt.title(f"Total Power: {total_W:.2f} W/m^2")
    plt.show()


        
#    phoE = (h_planck * c_light) / Lambda # Photon Energy E = hf, f = c/lambda
#     thermE = k_boltz * temp_k # thermal energy = kT

#     with np.errstate(over = 'ignore'):
#         boltzFactor = np.exp(phoE/thermE) #Planck distribution factor. It’s what gives the blackbody curve its distinct "hill" shape.
    
#         planckSpectral = C1*(1/(boltzFactor -1))


#     emissivity = selectiveEmit(energyBandGap, Lambda, materialProp["eps_high"], materialProp["eps_low"]) # Lambda is a vector or a np array
    
#     radiance = planckSpectral * emissivity

#     return np.trapezoid(radiance,Lambda) 