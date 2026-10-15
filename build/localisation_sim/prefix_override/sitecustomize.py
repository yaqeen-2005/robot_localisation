import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/yaqeen/robot_localisation_ws/install/localisation_sim'
