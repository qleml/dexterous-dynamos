import tkinter as tk
from tkinter import ttk, messagebox
import time
import sys
sys.path.insert(0, '/home/aristotelis/Desktop/ethCourses1st/realWorldRobotics/dexterous-dynamos/DynamixelControler')

from gripper_controller import GripperController
import numpy as np
import yaml
import os

DEFAULT_ANGLE = 0

class ServoControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Servo Control App")
        self.selected_servo = "Servo 1"
        self.servos = {
            "Servo 1": {"angle": DEFAULT_ANGLE, "id": 1},
            "Servo 2": {"angle": DEFAULT_ANGLE, "id": 2},
            "Servo 3": {"angle": DEFAULT_ANGLE, "id": 3},
            "Servo 4": {"angle": DEFAULT_ANGLE, "id": 4},
            "Servo 5": {"angle": DEFAULT_ANGLE, "id": 5},
            "Servo 6": {"angle": DEFAULT_ANGLE, "id": 6},
            "Servo 7": {"angle": DEFAULT_ANGLE, "id": 7},
            "Servo 8": {"angle": DEFAULT_ANGLE, "id": 8},
            "Servo 9": {"angle": DEFAULT_ANGLE, "id": 9},
            "Servo 10": {"angle": DEFAULT_ANGLE, "id": 10},
            "Servo 11": {"angle": DEFAULT_ANGLE, "id": 11},
            "Servo 12": {"angle": DEFAULT_ANGLE, "id": 12},
            "Servo 13": {"angle": DEFAULT_ANGLE, "id": 13},
            "Servo 14": {"angle": DEFAULT_ANGLE, "id": 14},
            "Servo 15": {"angle": DEFAULT_ANGLE, "id": 15},
            "Servo 16": {"angle": DEFAULT_ANGLE, "id": 16}}
        
        self.is_calibrating = False
        self.just_Calibrated = False

        self.gc = GripperController(port="/dev/ttyUSB0",calibration=False)
        servos_to_delete = []
        for servo in self.servos: 
            if self.servos[servo]['id'] not in self.gc.motor_ids:
                servos_to_delete.append(servo)

        for servo in servos_to_delete:
            del self.servos[servo]

        self.create_widgets()

    def create_widgets(self):
        # Servo Buttons
        self.label = tk.Label(self.root, text="Select a Servo:")
        self.label.pack(pady=10)


        # Create frames for left and right button groups
        button_frame_left = tk.Frame(self.root)
        button_frame_right = tk.Frame(self.root)

        button_frame_left.pack(side="left", padx=20, pady=10)
        button_frame_right.pack(side="right", padx=20, pady=10)

        # Add servo buttons on the left and right frames
        left_servos = list(self.servos.keys())[:8]  # First 8 servos
        right_servos = list(self.servos.keys())[8:]  # Last 8 servos

        for servo in left_servos:
            btn = ttk.Button(button_frame_left, text=servo, command=lambda s=servo: self.select_servo(s))
            btn.pack(pady=5)

        for servo in right_servos:
            btn = ttk.Button(button_frame_right, text=servo, command=lambda s=servo: self.select_servo(s))
            btn.pack(pady=5)

        # Angle Slider
        self.angle_label = tk.Label(self.root, text="Angle: {}".format(DEFAULT_ANGLE))
        self.angle_label.pack(pady=10)

        self.angle_slider = tk.Scale(self.root, from_=0, to=360, orient='horizontal', length=360, command=self.update_angle)
        self.angle_slider.set(DEFAULT_ANGLE)
        self.angle_slider.pack()

        # Reset Buttons
        self.reset_button = ttk.Button(self.root, text="Reset", command=self.reset_selected_servo)
        self.reset_button.pack(pady=10)

        self.reset_all_button = ttk.Button(self.root, text="Reset All", command=self.reset_all_servos)
        self.reset_all_button.pack(pady=10)

        # Calibrate Button
        self.calibrate_button = ttk.Button(self.root, text="Calibrate", command=self.start_calibration)
        self.calibrate_button.pack(pady=10)

        # Status Label
        self.status_label = tk.Label(self.root, text="No Servo Selected", font=("Helvetica", 12))
        self.status_label.pack(pady=20)

    def select_servo(self, servo):
        if self.is_calibrating:
            messagebox.showwarning("Calibration in progress", "Finish calibration before selecting another servo.")
            return
        
        self.selected_servo = servo
        self.status_label.config(text=f"Selected {servo}")

        # Set the current servo values in the sliders
        self.angle_slider.set(self.servos[servo]["angle"])

    def update_angle(self, value):
        if self.just_Calibrated:
            self.just_Calibrated = False
            return
        
        if self.selected_servo and not self.is_calibrating:
            self.servos[self.selected_servo]["angle"] = int(value) 
            self.angle_label.config(text=f"Angle: {value}")
            self.update_servo(self.selected_servo)


    def update_servo(self, servo):
        # Get motor positions 
        motor_pos_init = np.copy(self.gc.motor_id2init_pos)
        motor_pos_des  = self.gc.get_motor_pos()
        # Set desired motor position of selected servo
        id = self.servos[servo]["id"]
        motor_pos_des[id-1] = motor_pos_init[id-1] + np.deg2rad(self.servos[servo]['angle'])

        self.gc.write_desired_motor_pos(motor_pos_des)

        print(f"{servo} -> Angle: {self.servos[servo]['angle']}")

    def reset_selected_servo(self):
        if self.selected_servo:
            self.servos[self.selected_servo] = {"angle": DEFAULT_ANGLE, "id": self.servos[self.selected_servo]["id"]}
            self.angle_slider.set(DEFAULT_ANGLE)
            self.status_label.config(text=f"{self.selected_servo} reset to default values")
            self.update_servo(self.selected_servo)

    def reset_all_servos(self):
        servos_to_update_slider = []
        for servo in self.servos:
            id = self.servos[servo]['id']
            if id in self.gc.motor_ids:
                self.servos[servo] = {"angle": DEFAULT_ANGLE, "id": id}
                servos_to_update_slider.append(servo)
                print(f"{servo} will be reset")

        motor_pos_init = np.copy(self.gc.motor_id2init_pos)
        self.gc.wait_for_motion()
        self.gc.write_desired_motor_pos(motor_pos_init)
        self.gc.wait_for_motion()


    def start_calibration(self):
        if self.selected_servo:
            self.is_calibrating = True
            
            self.gc.disable_torque()
            self.status_label.config(text="Move fingers to init posiiton and press Enter to continue...")

            self.calibrate_button.config(text="Finish Calibration", command=self.finish_calibration)
            self.angle_slider.config(state='disabled')
        else:
            messagebox.showwarning("No Servo Selected", "Please select a servo before calibrating.")

    def finish_calibration(self):
        # Calibration Code is mostly taken from gripper_controller.py

        self.gc.motor_id2init_pos = self.gc.get_motor_pos()

        print(f"Motor positions after calibration: {self.gc.motor_id2init_pos}")

        maxCurrent = 150
        self.gc.motor_id2init_pos = self.gc.get_motor_pos()
        self.gc.set_operating_mode(5)
        self.gc.write_desired_motor_current(maxCurrent * np.ones(len(self.gc.motor_ids)))
        time.sleep(0.2)

        cal_yaml_fname = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cal.yaml")
        # Save the offsets to a YAML file
        with open(cal_yaml_fname, 'r') as cal_file:
            cal_orig = yaml.load(cal_file, Loader=yaml.FullLoader)

        cal_orig['motor_init_pos'] = self.gc.motor_id2init_pos.tolist()

        with open(cal_yaml_fname, 'w') as cal_file:
            yaml.dump(cal_orig, cal_file, default_flow_style=False)

        self.status_label.config(text=f"Calibration for {self.selected_servo} complete.")
        self.calibrate_button.config(text="Calibrate", command=self.start_calibration)
        
        self.is_calibrating  = False
        self.just_Calibrated = True
        self.servos[self.selected_servo] = {"angle": DEFAULT_ANGLE, "id": self.servos[self.selected_servo]["id"]}
        self.angle_slider.config(state='normal')        
        self.angle_slider.set(DEFAULT_ANGLE)


        self.angle_label.config(text=f"Angle: {DEFAULT_ANGLE}")
        
if __name__ == "__main__":
    root = tk.Tk()
    app = ServoControlApp(root)
    root.mainloop()
