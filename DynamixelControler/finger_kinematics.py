import numpy as np

 
finger_PIP_diameter = 15 #mm
finger_MCP_diameter = 15
finger_ABD_diameter = 18

def tendonlength_flexor_PIP(theta_PIP):
   '''Input: joint angle of PIP joint in rad
      Output: total normal lengths of flexor tendon through PIP joint'''
   return (finger_PIP_diameter/2)*theta_PIP

def tendonlength_extensor_PIP(theta_PIP):
   '''Input: joint angle of PIP joint in rad
      Output: total normal lengths of extensor tendon through PIP joint'''
   return (finger_PIP_diameter/2)*theta_PIP

def tendonlength_flexor_MCP(theta_MCP):
   '''Input: joint angle of MCP joint in rad
      Output: total normal lengths of flexor tendon through MCP joint'''
   return (finger_MCP_diameter/2)*theta_MCP

def tendonlength_extensor_MCP(theta_MCP):
   '''Input: joint angle of MCP joint in rad
      Output: total normal lengths of extensor tendon through MCP joint'''
   return (finger_MCP_diameter/2)*theta_MCP

def tendonlength_flexor_ABD(theta_ABD):
   # As flexor for ABD we consider the left abduction motion while looking at the palm
   '''Input: joint angle of ABD joint in rad
      Output: total normal lengths of flexor tendon through ABD joint'''
   return (finger_ABD_diameter/2)*theta_ABD

def tendonlength_extensor_ABD(theta_ABD):
   '''Input: joint angle of ABD joint in rad
      Output: total normal lengths of extensor tendon through ABD joint'''
   return (finger_ABD_diameter/2)*theta_ABD

def pose2tendon_finger(theta_PIP, theta_MCP, theta_ABD):
   '''Input: controllable joint angles
      Output: array of tendon lengths for given joint angles'''
   return [tendonlength_flexor_PIP(theta_PIP),
            tendonlength_extensor_PIP(theta_PIP),
            tendonlength_flexor_MCP(theta_MCP), 
            tendonlength_extensor_MCP(theta_MCP),
            tendonlength_flexor_ABD(theta_ABD),
            tendonlength_extensor_ABD(theta_ABD)]












# def tendonlength_flexor_joint1(theta_joint1):
#    '''Input: joint angle of joint1 in rad
#       Output: total normal lengths of flexor tendon through joint1'''
#    return np.sqrt(6.4**2 + 5.2**2 - 2*6.4*5.2*np.cos(1.92-theta_joint1))

# def tendonlength_extensor_joint1(theta_joint1):
#    '''Input: joint angle of joint1 in rad
#       Output: total normal lengths of extensor tendon through joint1'''
#    return np.sqrt(5.4**2 + 4.8**2 - 2*5.4*4.8*np.cos(1.92+theta_joint1))

# def tendonlength_flexor_joint2(theta_joint2):
#    '''Input: joint angle of joint2 in rad
#       Output: total normal lengths of flexor tendon through joint2'''
#    return np.sqrt(5.7**2 + 4.8**2 - 2*5.7*4.8*np.cos(1.81-theta_joint2))

# def tendonlength_extensor_joint2(theta_joint2):
#    '''Input: joint angle of joint2 in rad
#       Output: total normal lengths of extensor tendon through joint2'''
#    return np.sqrt(4.9**2 + 4.4**2 - 2*4.9*4.4*np.cos(1.81+theta_joint2))
