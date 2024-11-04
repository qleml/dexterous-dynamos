#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
import numpy as np
import sys
sys.path.insert(0, '/home/aristotelis/Desktop/ethCourses1st/realWorldRobotics/dexterous-dynamos/DynamixelControler')
import os
from gripper_controller import GripperController
import yaml

# Numbers correspond to position in list self.joint_angles and their range limits
# The id's here do not make sense. The corespond on how they are defined in the gripper_defs.yaml file.
# For example 0 means the first defined motor on the yaml file 
# 1 the second defined etc. 

def load_joint_map_from_yaml():
    current_dir = os.path.abspath(__file__)
    previous_directory = os.path.dirname(os.path.dirname(current_dir))
    gripper_defs_path = os.path.join(previous_directory, "gripper_defs.yaml")
    with open(gripper_defs_path, 'r') as file:
        data = yaml.safe_load(file)
    
    joint_map = {}
    joint_type = ['pip-dip', 'mcp', 'abd']
    for finger, details in data['muscle_groups'].items():
        joint_map[finger] = {}
        for i, motor_id in enumerate(details['motor_ids']):
            if i<3:
                joint_map[finger].update({'{}_{}'.format(finger,joint_type[i]): details['joint_roms'][i]})
            else:
                joint_map[finger].update({'{}_joint_{}'.format(finger,i): details['joint_roms'][i]})
        
    return joint_map

class GuiInterface:
    def __init__(self, master):
        # self.gc = GripperController(port="/dev/ttyUSB0",calibration=True)
        
        # Data storage
        self.number_of_joints = 16
        self.master = master

        # GUI elements 
        self.master.title("GUI Control") 

        # Create main frames for sliders and buttons
        self.sliders_frame = ttk.Frame(master)
        self.buttons_frame = ttk.Frame(master)

        # Pack the main frames
        self.sliders_frame.pack(side=tk.LEFT, fill="both", expand=True)
        self.buttons_frame.pack(side=tk.RIGHT, fill="both", expand=True)


        self.joint_angles = [0] * self.number_of_joints
        self.value_labels = [None] * len(self.joint_angles)
        self.sliders = [None] * len(self.joint_angles)
        self.hand_finger_joint_map = load_joint_map_from_yaml()

        # Creating the GUI components
        for i, finger_key in enumerate(self.hand_finger_joint_map):
            group_frame = ttk.LabelFrame(self.sliders_frame, text=f"{finger_key}")
            group_frame.pack(padx=10, pady=10, fill="both", expand="yes")
            self.create_slider_group(group_frame, i, finger_key)

    def create_slider_group(self, frame, group_index, finger):
        finger_subcomponents_map = self.hand_finger_joint_map[finger]

        for j, finger_subcomponent_key in enumerate(finger_subcomponents_map):
            # Create frame for each slider and value label
            slider_frame = ttk.Frame(frame)
            slider_frame.pack(pady=5)

            # Create and pack the slider 
            slider_label = ttk.Label(frame, text=f"{finger_subcomponent_key}")
            slider_label.pack(pady=5)

            # Create and pack the slider 
            slider_index = j
            slider_limit_min, slider_limit_max = finger_subcomponents_map[finger_subcomponent_key]        
            slider = ttk.Scale(slider_frame, from_=slider_limit_min, to_=slider_limit_max, orient='horizontal', length= 360)

            slider.pack(side=tk.LEFT, padx=5)
            slider.bind("<B1-Motion>", lambda event, index=slider_index: self.update_slider_value(event.widget.get(), index))

            # Storing the slider for later access
            self.sliders[slider_index] = slider

            # Create and pack the value label 
            value_label = ttk.Label(slider_frame, text="0")
            value_label.pack(side=tk.LEFT, padx=5)

            max_min_label = ttk.Label(slider_frame, text="ROM: {}~{} degrees".format(slider_limit_min, slider_limit_max))
            max_min_label.pack(side=tk.LEFT, padx=5)

            # Store the value label in a dictionary for later access
            self.value_labels[slider_index] = value_label

    def update_slider_value(self, value, index):
        self.joint_angles[index] = float(value)
        self.value_labels[index].config(text=f"{value:.2f}")
        self.gc.write_desired_joint_angles(self.joint_angles)



if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x750")
    app = GuiInterface(root)
    root.mainloop()










    # def set_preprogrammed_movement(self, angles):
    #     for i, angle in enumerate(angles):
    #         self.joint_angles[i] = angle
    #         if self.sliders[i] is not None:
    #             self.sliders[i].set(angle)
    #         if self.value_labels[i] is not None:
    #             self.value_labels[i].config(text=f"{angle:.2f}")

    #     # Immediately publish the new joint angles
    #     self.publish_joint_angles()

    # def publish_joint_angles(self):
    #     return
        # if self.just_Calibrated:
        #     self.just_Calibrated = False
        #     return
        
        # if self.selected_servo and not self.is_calibrating:
        #     self.servos[self.selected_servo]["angle"] = int(value) 
        #     self.angle_label.config(text=f"Angle: {value}")
        #     self.update_servo(self.selected_servo)      

        # msg = Float32MultiArray()
        # msg.data = self.joint_angles
        # self.cmd_joint_angles_pub.publish(msg)