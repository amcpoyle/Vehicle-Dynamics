import pandas as pd
import numpy as np
import locale
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter as tk

def main():

    # setup
    locale.setlocale(locale.LC_ALL, '')

    # dir_path = "chassisArmSizing_example1.csv"
    # dir_df = pd.read_csv(dir_path)
    dir_path = None
    dir_df = None

    braking_path = None
    braking_df = None

    cornering_path = None
    cornering_df = None

    accel_path = None
    accel_df = None

    bump_path = None
    bump_df = None

    tdFRLF = None
    tdFRLA = None
    tdFRTR = None
    tdFRCO = None
    ttFRLF = None
    ttFRLA = None
    ttFRTR = None
    ttFRCO = None

    lower_upper = None
    right_left = None
    front_rear = None

    currentCorner = None

    # central variables
    elastic_modulus = 132300000 # n/in^2
    tensile_yield = 280645 # n/in^2

    def updateInputVars(*args):
        # called whenever a variable is changed
        global tdFRLF, tdFRLA, tdFRTR, tdFRCO
        global ttFRLF, ttFRLA, ttFRTR, ttFRCO

        tdFRLF = tubeDiameterEntry_FRLF_var.get()
        tdFRLA = tubeDiameterEntry_FRLA_var.get()
        tdFRTR = tubeDiameterEntry_FRTR_var.get()
        tdFRCO = tubeDiameterEntry_FRCO_var.get()

        ttFRLF = tubeThicknessEntry_FRLF_var.get()
        ttFRLA = tubeThicknessEntry_FRLA_var.get()
        ttFRTR = tubeThicknessEntry_FRTR_var.get()
        ttFRCO = tubeThicknessEntry_FRCO_var.get()

    def updateCurrentCorner(cornerName):
        global currentCorner
        currentCorner = cornerName

    def directionUploadAction(event=None):
        global dir_path
        filename = filedialog.askopenfilename()
        dir_path = filename

    def brakingUploadAction(event=None):
        global braking_path
        filename = filedialog.askopenfilename()
        braking_path = filename

    def corneringUploadAction(event=None):
        global cornering_path
        filename = filedialog.askopenfilename()
        cornering_path = filename

    def accelUploadAction(event=None):
        global accel_path
        filename = filedialog.askopenfilename()
        accel_path = filename

    def bumpUploadAction(event=None):
        global bump_path
        filename = filedialog.askopenfilename()
        bump_path = filename

    def createResultsFrame(FRLF, FRLA, FRTR, FRCO):
        global currentCorner
        global lower_upper, front_rear, right_left
        FRLF_data = []
        FRLA_data = []
        FRTR_data = []
        FRCO_data = []
        for i in FRLF.values():
            try:
                FRLF_data.append(round(i, 9))
            except:
                FRLF_data.append(i)
        for i in FRLA.values():
            try:
                FRLA_data.append(round(i, 9))
            except:
                FRLA_data.append(i)
        for i in FRTR.values():
            try:
                FRTR_data.append(round(i, 9))
            except:
                FRTR_data.append(i)
        for i in FRCO.values():
            try:
                FRCO_data.append(round(i, 9))
            except:
                FRCO_data.append(i)

            

        new_frm = tk.Toplevel(root)
        new_frm.title("Control Arm Sizing Results: {}".format(currentCorner))
        new_frm.geometry("1000x400")
        height = 5 # rows
        width = 11 # columns
        row1_data = ['Results', 'Minimum I', 'Minimum Area', 'r1', 'r2', 'I (from r1 r2)', 'I',
                    'FoS (I)', 'Area', 'FoS (A)', 'Weight']
        row2_data = ['{}{}{}F'.format(front_rear, right_left, lower_upper)] + FRLF_data # need to change to make frlf, frla, frtr a variable
        row3_data = ['{}{}{}A'.format(front_rear, right_left, lower_upper)] + FRLA_data
        row4_data = ['{}{}TR'.format(front_rear, right_left)] + FRTR_data
        row5_data = ['{}{}CO'.format(front_rear, right_left)] + FRCO_data
        table = [row1_data, row2_data, row3_data, row4_data, row5_data]


        for i in range(height): # iterate through rows
            for j in range(width): # iterate through columns
                ttk.Label(new_frm, text=table[i][j], padding=(20, 10)).grid(row=i, column=j)


    def RunApp(event=None):
        global dir_df, braking_df, cornering_df, accel_df, bump_df
        global tdFRLF, tdFRLA, tdFRTR, tdFRCO
        global ttFRLF, ttFRLA, ttFRTR, ttFRCO
        global currentCorner
        global lower_upper, right_left, front_rear


        # defining row names based on currentCorner
        if currentCorner == 'FLU':
            lower_upper = "Upper"
            right_left = "Left"
            front_rear = "Front"
        elif currentCorner == 'FLL':
            lower_upper = "Lower"
            right_left = "Left"
            front_rear = "Front"
        elif currentCorner == 'FRU':
            lower_upper = "Upper"
            right_left = "Right"
            front_rear = "Front"
        elif currentCorner == 'FRL':
            lower_upper = "Lower"
            right_left = "Right"
            front_rear = "Front"
        elif currentCorner == 'RLU':
            lower_upper = "Upper"
            right_left = "Left"
            front_rear = "Rear"
        elif currentCorner == 'RLL':
            lower_upper = "Lower"
            right_left = "Left"
            front_rear = "Rear"
        elif currentCorner == 'RRU':
            lower_upper = "Upper"
            right_left = "Right"
            front_rear = "Rear"
        elif currentCorner == 'RRL':
            lower_upper = "Lower"
            right_left = "Right"
            front_rear = "Rear"
        else:
            # should never reach here
            currentCorner = "error"



        tube_diameters = {'FRLF': float(tdFRLF), 'FRLA': float(tdFRLA), 'FRTR': float(tdFRTR), 'FRCO': float(tdFRCO)}
        tube_thicknesses = {'FRLF': float(ttFRLF), 'FRLA': float(ttFRLA), 'FRTR': float(ttFRTR), 'FRCO': float(ttFRCO)}

        dir_df = pd.read_csv(dir_path)
        braking_df = pd.read_csv(braking_path)
        cornering_df = pd.read_csv(cornering_path)
        accel_df = pd.read_csv(accel_path)
        bump_df = pd.read_csv(bump_path)

        dir_target_row = dir_df.iloc[-1]
        braking_target_row = braking_df.iloc[-1]
        cornering_target_row = cornering_df.iloc[-1]
        accel_target_row = accel_df.iloc[-1]
        bump_target_row = bump_df.iloc[-1]

        target_rows = {'dir': dir_target_row, 'braking': braking_target_row, 'cornering': cornering_target_row,
                        'accel': accel_target_row, 'bump': bump_target_row}

        # direction values need a little more changing
        # push rod -> coil over
        # note: upright - chassis


        iterable_categories = ['dir', 'braking', 'cornering', 'accel', 'bump', 'cornering and bump', 'accel and bump', 'braking and bump']

        # length_frlf = None
        # length_frla = None
        # length_FRTR = None

        # dir_FRLF_X = 281.25
        # dir_FRLF_Y = 26.96
        # dir_FRLF_Z = -150.23
        # dir_FRLA_X = 278.13
        # dir_FRLA_Y = 26.68
        # dir_FRLA_Z = 145.45
        # dir_FRCO_X = 473.52
        # dir_FRCO_Y = -428.9
        # dir_FRCO_Z = -66.46

        vars = {'braking': {'FRLF': {'X': None, 'Y': None, 'Z': None}, 'FRLA': {'X': None, 'Y': None, 'Z': None}, 'FRTR': {'X': None, 'Y': None, 'Z': None}, 'FRCO': {'X': None, 'Y': None, 'Z': None}},
                'cornering': {'FRLF': {'X': None, 'Y': None, 'Z': None}, 'FRLA': {'X': None, 'Y': None, 'Z': None}, 'FRTR': {'X': None, 'Y': None, 'Z': None}, 'FRCO': {'X': None, 'Y': None, 'Z': None}},
                'accel': {'FRLF': {'X': None, 'Y': None, 'Z': None}, 'FRLA': {'X': None, 'Y': None, 'Z': None}, 'FRTR': {'X': None, 'Y': None, 'Z': None}, 'FRCO': {'X': None, 'Y': None, 'Z': None}},
                'bump': {'FRLF': {'X': None, 'Y': None, 'Z': None}, 'FRLA': {'X': None, 'Y': None, 'Z': None}, 'FRTR': {'X': None, 'Y': None, 'Z': None}, 'FRCO': {'X': None, 'Y': None, 'Z': None}},
                'dir': {'FRLF': {'X': None, 'Y': None, 'Z': None}, 'FRLA': {'X': None, 'Y': None, 'Z': None}, 'FRTR': {'X': None, 'Y': None, 'Z': None}, 'FRCO': {'X': None, 'Y': None, 'Z': None}},
                'cornering and bump': {'FRLF': {'X': None, 'Y': None, 'Z': None}, 'FRLA': {'X': None, 'Y': None, 'Z': None}, 'FRTR': {'X': None, 'Y': None, 'Z': None}, 'FRCO': {'X': None, 'Y': None, 'Z': None}},
                'accel and bump': {'FRLF': {'X': None, 'Y': None, 'Z': None}, 'FRLA': {'X': None, 'Y': None, 'Z': None}, 'FRTR': {'X': None, 'Y': None, 'Z': None}, 'FRCO': {'X': None, 'Y': None, 'Z': None}},
                'braking and bump': {'FRLF': {'X': None, 'Y': None, 'Z': None}, 'FRLA': {'X': None, 'Y': None, 'Z': None}, 'FRTR': {'X': None, 'Y': None, 'Z': None}, 'FRCO': {'X': None, 'Y': None, 'Z': None}}
                }

        # directions
        vars['dir']['FRLF']['X'] = dir_target_row['{} A-Arm Upright X [{}] [{}]'.format(lower_upper, right_left, front_rear)] - dir_target_row['{} A-Arm Chassis Fore X [{}] [{}]'.format(lower_upper, right_left, front_rear)]
        vars['dir']['FRLF']['Y'] = dir_target_row['{} A-Arm Upright Y [{}] [{}]'.format(lower_upper, right_left, front_rear)] - dir_target_row['{} A-Arm Chassis Fore Y [{}] [{}]'.format(lower_upper, right_left, front_rear)]
        vars['dir']['FRLF']['Z'] = dir_target_row['{} A-Arm Upright Z [{}] [{}]'.format(lower_upper, right_left, front_rear)] - dir_target_row['{} A-Arm Chassis Fore Z [{}] [{}]'.format(lower_upper, right_left, front_rear)]

        vars['dir']['FRLA']['X'] = dir_target_row['{} A-Arm Upright X [{}] [{}]'.format(lower_upper, right_left, front_rear)] - dir_target_row['{} A-Arm Chassis Aft X [{}] [{}]'.format(lower_upper, right_left, front_rear)]
        vars['dir']['FRLA']['Y'] = dir_target_row['{} A-Arm Upright Y [{}] [{}]'.format(lower_upper, right_left, front_rear)] - dir_target_row['{} A-Arm Chassis Aft Y [{}] [{}]'.format(lower_upper, right_left, front_rear)]
        vars['dir']['FRLA']['Z'] = dir_target_row['{} A-Arm Upright Z [{}] [{}]'.format(lower_upper, right_left, front_rear)] - dir_target_row['{} A-Arm Chassis Aft Z [{}] [{}]'.format(lower_upper, right_left, front_rear)]

        if front_rear == 'Front':
            vars['dir']['FRTR']['X'] = dir_target_row['Tie Rod Chassis X [{}] [{}]'.format(right_left, front_rear)] - dir_target_row['Tie Rod Upright X [{}] [{}]'.format(right_left, front_rear)]
            vars['dir']['FRTR']['Y'] = dir_target_row['Tie Rod Chassis Y [{}] [{}]'.format(right_left, front_rear)] - dir_target_row['Tie Rod Upright Y [{}] [{}]'.format(right_left, front_rear)]
            vars['dir']['FRTR']['Z'] = dir_target_row['Tie Rod Chassis Z [{}] [{}]'.format(right_left, front_rear)] - dir_target_row['Tie Rod Upright Z [{}] [{}]'.format(right_left, front_rear)]

            vars['dir']['FRCO']['X'] = dir_target_row['CoilOver Chassis X [{}] [{}]'.format(right_left, front_rear)] - dir_target_row['CoilOver Outer X [{}] [{}]'.format(right_left, front_rear)]
            vars['dir']['FRCO']['Y'] = dir_target_row['CoilOver Chassis Y [{}] [{}]'.format(right_left, front_rear)] - dir_target_row['CoilOver Outer Y [{}] [{}]'.format(right_left, front_rear)]
            vars['dir']['FRCO']['Z'] = dir_target_row['CoilOver Chassis Z [{}] [{}]'.format(right_left, front_rear)] - dir_target_row['CoilOver Outer Z [{}] [{}]'.format(right_left, front_rear)]
        else:
            vars['dir']['FRTR']['X'] = dir_target_row['Tie Rod Chassis X [{}] [{}]'.format(right_left, front_rear)] - dir_target_row['Tie Rod Upright X [{}] [{}]'.format(right_left, front_rear)]
            vars['dir']['FRTR']['Y'] = dir_target_row['Tie Rod Chassis Y [{}] [{}]'.format(right_left, front_rear)] - dir_target_row['Tie Rod Upright Y [{}] [{}]'.format(right_left, front_rear)]
            vars['dir']['FRTR']['Z'] = dir_target_row['Tie Rod Chassis Z [{}] [{}]'.format(right_left, front_rear)] - dir_target_row['Tie Rod Upright Z [{}] [{}]'.format(right_left, front_rear)]

            # TODO: should be outer - chassis?
            vars['dir']['FRCO']['X'] = dir_target_row['CoilOver Chassis X [{}] [{}]'.format(right_left, front_rear)] - dir_target_row['CoilOver Outer X [{}] [{}]'.format(right_left, front_rear)]
            vars['dir']['FRCO']['Y'] = dir_target_row['CoilOver Chassis Y [{}] [{}]'.format(right_left, front_rear)] - dir_target_row['CoilOver Outer Y [{}] [{}]'.format(right_left, front_rear)]
            vars['dir']['FRCO']['Z'] = dir_target_row['CoilOver Chassis Z [{}] [{}]'.format(right_left, front_rear)] - dir_target_row['CoilOver Outer Z [{}] [{}]'.format(right_left, front_rear)]


        print(vars['dir']['FRCO'])
        # forces
        for i in iterable_categories:
            if i == 'dir':
                continue
            # ALSO: Upper A-Arm
            # left hand turn --> right tires are outer tires

            # chassis to lower a-arm goes out direction
            if 'and bump' in i:
                # add forces
                force_name = i.split(' ')[0]
                if lower_upper == 'Upper':
                    vars[i]['FRLF']['X'] = vars[force_name]['FRLF']['X'] + vars['bump']['FRLF']['X']
                    vars[i]['FRLF']['Y'] = vars[force_name]['FRLF']['Y'] + vars['bump']['FRLF']['Y']
                    vars[i]['FRLF']['Z'] = vars[force_name]['FRLF']['Z'] + vars['bump']['FRLF']['Z']

                    vars[i]['FRLA']['X'] = vars[force_name]['FRLA']['X'] + vars['bump']['FRLA']['X']
                    vars[i]['FRLA']['Y'] = vars[force_name]['FRLA']['Y'] + vars['bump']['FRLA']['Y']
                    vars[i]['FRLA']['Z'] = vars[force_name]['FRLA']['Z'] + vars['bump']['FRLA']['Z']

                    vars[i]['FRTR']['X'] = None
                    vars[i]['FRTR']['Y'] = None
                    vars[i]['FRTR']['Z'] = None

                    vars[i]['FRCO']['X'] = vars[force_name]['FRCO']['X'] + vars['bump']['FRCO']['X']
                    vars[i]['FRCO']['Y'] = vars[force_name]['FRCO']['Y'] + vars['bump']['FRCO']['Y']
                    vars[i]['FRCO']['Z'] = vars[force_name]['FRCO']['Z'] + vars['bump']['FRCO']['Z']
                else:
                    vars[i]['FRLF']['X'] = vars[force_name]['FRLF']['X'] + vars['bump']['FRLF']['X']
                    vars[i]['FRLF']['Y'] = vars[force_name]['FRLF']['Y'] + vars['bump']['FRLF']['Y']
                    vars[i]['FRLF']['Z'] = vars[force_name]['FRLF']['Z'] + vars['bump']['FRLF']['Z']

                    vars[i]['FRLA']['X'] = vars[force_name]['FRLA']['X'] + vars['bump']['FRLA']['X']
                    vars[i]['FRLA']['Y'] = vars[force_name]['FRLA']['Y'] + vars['bump']['FRLA']['Y']
                    vars[i]['FRLA']['Z'] = vars[force_name]['FRLA']['Z'] + vars['bump']['FRLA']['Z']

                    vars[i]['FRTR']['X'] = vars[force_name]['FRTR']['X'] + vars['bump']['FRTR']['X']
                    vars[i]['FRTR']['Y'] = vars[force_name]['FRTR']['Y'] + vars['bump']['FRTR']['Y']
                    vars[i]['FRTR']['Z'] = vars[force_name]['FRTR']['Z'] + vars['bump']['FRTR']['Z']

                    vars[i]['FRCO']['X'] = None
                    vars[i]['FRCO']['Y'] = None
                    vars[i]['FRCO']['Z'] = None

            else: # not a bump case
                if front_rear == 'Front':
                    if lower_upper == 'Upper':
                        # only pull rod
                        # NOTE: use to be chassis to
                        vars[i]['FRLF']['X'] = target_rows[i]['{} A-Arm To Chassis (Fore) - Fx [{} {}]'.format(lower_upper, front_rear, right_left)]
                        vars[i]['FRLF']['Y'] = target_rows[i]['{} A-Arm To Chassis (Fore) - Fy [{} {}]'.format(lower_upper, front_rear, right_left)]
                        vars[i]['FRLF']['Z'] = target_rows[i]['{} A-Arm To Chassis (Fore) - Fz [{} {}]'.format(lower_upper, front_rear, right_left)]

                        vars[i]['FRLA']['X'] = target_rows[i]['{} A-Arm To Chassis (Aft) - Fx [{} {}]'.format(lower_upper, front_rear, right_left)]
                        vars[i]['FRLA']['Y'] = target_rows[i]['{} A-Arm To Chassis (Aft) - Fy [{} {}]'.format(lower_upper, front_rear, right_left)]
                        vars[i]['FRLA']['Z'] = target_rows[i]['{} A-Arm To Chassis (Aft) - Fz [{} {}]'.format(lower_upper, front_rear, right_left)]

                        vars[i]['FRTR']['X'] = None
                        vars[i]['FRTR']['Y'] = None
                        vars[i]['FRTR']['Z'] = None

                        # pull rod data isn't right in the excel spreadsheet
                        vars[i]['FRCO']['X'] = target_rows[i]['CoilOver To Chassis - Fx [{} {}]'.format(front_rear, right_left)]
                        vars[i]['FRCO']['Y'] = target_rows[i]['CoilOver To Chassis - Fy [{} {}]'.format(front_rear, right_left)]
                        vars[i]['FRCO']['Z'] = target_rows[i]['CoilOver To Chassis - Fz [{} {}]'.format(front_rear, right_left)]
                    
                    else:
                        # only tie rod

                        vars[i]['FRLF']['X'] = target_rows[i]['{} A-Arm To Chassis (Fore) - Fx [{} {}]'.format(lower_upper, front_rear, right_left)]
                        vars[i]['FRLF']['Y'] = target_rows[i]['{} A-Arm To Chassis (Fore) - Fy [{} {}]'.format(lower_upper, front_rear, right_left)]
                        vars[i]['FRLF']['Z'] = target_rows[i]['{} A-Arm To Chassis (Fore) - Fz [{} {}]'.format(lower_upper, front_rear, right_left)]

                        vars[i]['FRLA']['X'] = target_rows[i]['{} A-Arm To Chassis (Aft) - Fx [{} {}]'.format(lower_upper, front_rear, right_left)]
                        vars[i]['FRLA']['Y'] = target_rows[i]['{} A-Arm To Chassis (Aft) - Fy [{} {}]'.format(lower_upper, front_rear, right_left)]
                        vars[i]['FRLA']['Z'] = target_rows[i]['{} A-Arm To Chassis (Aft) - Fz [{} {}]'.format(lower_upper, front_rear, right_left)]

                        vars[i]['FRTR']['X'] = target_rows[i]['Tierod To Steering Rack - Fx [{} {}]'.format(front_rear, right_left)]
                        vars[i]['FRTR']['Y'] = target_rows[i]['Tierod To Steering Rack - Fy [{} {}]'.format(front_rear, right_left)]
                        vars[i]['FRTR']['Z'] = target_rows[i]['Tierod To Steering Rack - Fz [{} {}]'.format(front_rear, right_left)]

                        vars[i]['FRCO']['X'] = None
                        vars[i]['FRCO']['Y'] = None
                        vars[i]['FRCO']['Z'] = None

                else:
                    # rear
                    if lower_upper == 'Upper':
                        vars[i]['FRLF']['X'] = target_rows[i]['{} A-Arm To Chassis (Fore) - Fx [{} {}]'.format(lower_upper, front_rear, right_left)]
                        vars[i]['FRLF']['Y'] = target_rows[i]['{} A-Arm To Chassis (Fore) - Fy [{} {}]'.format(lower_upper, front_rear, right_left)]
                        vars[i]['FRLF']['Z'] = target_rows[i]['{} A-Arm To Chassis (Fore) - Fz [{} {}]'.format(lower_upper, front_rear, right_left)]

                        vars[i]['FRLA']['X'] = target_rows[i]['{} A-Arm To Chassis (Aft) - Fx [{} {}]'.format(lower_upper, front_rear, right_left)]
                        vars[i]['FRLA']['Y'] = target_rows[i]['{} A-Arm To Chassis (Aft) - Fy [{} {}]'.format(lower_upper, front_rear, right_left)]
                        vars[i]['FRLA']['Z'] = target_rows[i]['{} A-Arm To Chassis (Aft) - Fz [{} {}]'.format(lower_upper, front_rear, right_left)]

                        vars[i]['FRTR']['X'] = None
                        vars[i]['FRTR']['Y'] = None
                        vars[i]['FRTR']['Z'] = None

                        vars[i]['FRCO']['X'] = target_rows[i]['CoilOver To Chassis - Fx [{} {}]'.format(front_rear, right_left)]
                        vars[i]['FRCO']['Y'] = target_rows[i]['CoilOver To Chassis - Fy [{} {}]'.format(front_rear, right_left)]
                        vars[i]['FRCO']['Z'] = target_rows[i]['CoilOver To Chassis - Fz [{} {}]'.format(front_rear, right_left)]
                    else:
                        vars[i]['FRLF']['X'] = target_rows[i]['{} A-Arm To Chassis (Fore) - Fx [{} {}]'.format(lower_upper, front_rear, right_left)]
                        vars[i]['FRLF']['Y'] = target_rows[i]['{} A-Arm To Chassis (Fore) - Fy [{} {}]'.format(lower_upper, front_rear, right_left)]
                        vars[i]['FRLF']['Z'] = target_rows[i]['{} A-Arm To Chassis (Fore) - Fz [{} {}]'.format(lower_upper, front_rear, right_left)]

                        vars[i]['FRLA']['X'] = target_rows[i]['{} A-Arm To Chassis (Aft) - Fx [{} {}]'.format(lower_upper, front_rear, right_left)]
                        vars[i]['FRLA']['Y'] = target_rows[i]['{} A-Arm To Chassis (Aft) - Fy [{} {}]'.format(lower_upper, front_rear, right_left)]
                        vars[i]['FRLA']['Z'] = target_rows[i]['{} A-Arm To Chassis (Aft) - Fz [{} {}]'.format(lower_upper, front_rear, right_left)]

                        vars[i]['FRTR']['X'] = target_rows[i]['Tierod To Chassis - Fx [{} {}]'.format(front_rear, right_left)]
                        vars[i]['FRTR']['Y'] = target_rows[i]['Tierod To Chassis - Fy [{} {}]'.format(front_rear, right_left)]
                        vars[i]['FRTR']['Z'] = target_rows[i]['Tierod To Chassis - Fz [{} {}]'.format(front_rear, right_left)]

                        vars[i]['FRCO']['X'] = None
                        vars[i]['FRCO']['Y'] = None
                        vars[i]['FRCO']['Z'] = None

        print()
        print('CORNERING: ', vars['cornering'])
        print()


        # length_frlf_mm = np.sqrt(vars['dir']['FRLF']['X']**2 + vars['dir']['FRLF']['Y']**2 + vars['dir']['FRLF']['Z']**2)
        # length_frla_mm = np.sqrt(vars['dir']['FRLA']['X']**2 + vars['dir']['FRLA']['Y']**2 + vars['dir']['FRLA']['Z']**2)
        # length_FRTR_mm = np.sqrt(vars['dir']['FRTR']['X']**2 + vars['dir']['FRTR']['Y']**2 + vars['dir']['FRTR']['Z']**2)
        length_frlf_mm = np.sqrt(vars['dir']['FRLF']['X']**2 + vars['dir']['FRLF']['Y']**2 + vars['dir']['FRLF']['Z']**2)
        length_frla_mm = np.sqrt(vars['dir']['FRLA']['X']**2 + vars['dir']['FRLA']['Y']**2 + vars['dir']['FRLA']['Z']**2)
        length_FRTR_mm = np.sqrt(vars['dir']['FRTR']['X']**2 + vars['dir']['FRTR']['Y']**2 + vars['dir']['FRTR']['Z']**2)
        length_frco_mm = np.sqrt(vars['dir']['FRCO']['X']**2 + vars['dir']['FRCO']['Y']**2 + vars['dir']['FRCO']['Z']**2)

        length_frlf_in = length_frlf_mm/25.4
        length_frla_in = length_frla_mm/25.4
        length_FRTR_in = length_FRTR_mm/25.4
        length_frco_in = length_frco_mm/25.4

        print('LENGTHS: ', length_frlf_in)
        print('LENGTHS: ', length_frla_in)
        print('LENGTHS: ', length_FRTR_in)
        print("LENGTHS: ", length_frco_in)

        # TODO: 2 upper, 2 lower, 1 tie rod, 1 push rod (coil over)
        # for each case

        comp_tension = {'braking': {'FRLF': {'X': None, 'Y': None, 'Z': None}, # E F G 
                        'FRLA': {'X': None, 'Y': None, 'Z': None}, 
                        'FRTR': {'X': None, 'Y': None, 'Z': None},
                        'FRCO': {'X': None, 'Y': None, 'Z': None}}, 
            'cornering': {'FRLF': {'X': None, 'Y': None, 'Z': None}, 
                        'FRLA': {'X': None, 'Y': None, 'Z': None}, 
                        'FRTR': {'X': None, 'Y': None, 'Z': None},
                        'FRCO': {'X': None, 'Y': None, 'Z': None}}, 
            'accel': {'FRLF': {'X': None, 'Y': None, 'Z': None}, 
                        'FRLA': {'X': None, 'Y': None, 'Z': None}, 
                        'FRTR': {'X': None, 'Y': None, 'Z': None},
                        'FRCO': {'X': None, 'Y': None, 'Z': None}}, 
            'bump': {'FRLF': {'X': None, 'Y': None, 'Z': None}, 
                        'FRLA': {'X': None, 'Y': None, 'Z': None}, 
                        'FRTR': {'X': None, 'Y': None, 'Z': None},
                        'FRCO': {'X': None, 'Y': None, 'Z': None}},
            'cornering and bump': {'FRLF': {'X': None, 'Y': None, 'Z': None}, 
                        'FRLA': {'X': None, 'Y': None, 'Z': None}, 
                        'FRTR': {'X': None, 'Y': None, 'Z': None},
                        'FRCO': {'X': None, 'Y': None, 'Z': None}},
            'accel and bump': {'FRLF': {'X': None, 'Y': None, 'Z': None}, 
                        'FRLA': {'X': None, 'Y': None, 'Z': None}, 
                        'FRTR': {'X': None, 'Y': None, 'Z': None},
                        'FRCO': {'X': None, 'Y': None, 'Z': None}},
            'braking and bump': {'FRLF': {'X': None, 'Y': None, 'Z': None}, 
                        'FRLA': {'X': None, 'Y': None, 'Z': None}, 
                        'FRTR': {'X': None, 'Y': None, 'Z': None},
                        'FRCO': {'X': None, 'Y': None, 'Z': None}}
            }

        # setting E, F, G variables
        for i in iterable_categories: # braking, cornering, etc.
            if i == 'dir':
                continue

            # setting COMPRESSION and TENSION cases based on directions
            for j in ['X', 'Y', 'Z']:

                # checking if cornering force and direction is in the same direction ==> compression
                if ((vars[i]['FRLF'][j] > 0) & (vars['dir']['FRLF'][j] > 0)) | ((vars[i]['FRLF'][j] < 0) & (vars['dir']['FRLF'][j] < 0)):
                    comp_tension[i]['FRLF'][j] = 'compression'
                # if they are in opposite directions, then tension
                elif ((vars[i]['FRLF'][j] < 0) & (vars['dir']['FRLF'][j] > 0)) | ((vars[i]['FRLF'][j] > 0) & (vars['dir']['FRLF'][j] < 0)):
                    comp_tension[i]['FRLF'][j] = 'tension'
                # should never get here
                else:
                    comp_tension[i]['FRLF'][j] = 'error'

                # same thing as above but for aft
                if ((vars[i]['FRLA'][j] > 0) & (vars['dir']['FRLA'][j] > 0)) | ((vars[i]['FRLA'][j] < 0) & (vars['dir']['FRLA'][j] < 0)):
                    comp_tension[i]['FRLA'][j] = 'compression'
                elif ((vars[i]['FRLA'][j] < 0) & (vars['dir']['FRLA'][j] > 0)) | ((vars[i]['FRLA'][j] > 0) & (vars['dir']['FRLA'][j] < 0)):
                    comp_tension[i]['FRLA'][j] = 'tension'
                else:
                    comp_tension[i]['FRLA'][j] = 'error'

                # same thing but for tie rod
                if lower_upper == 'Lower':
                    comp_tension[i]['FRCO'][j] = 'error'
                    if ((vars[i]['FRTR'][j] > 0) & (vars['dir']['FRTR'][j] > 0)) | ((vars[i]['FRTR'][j] < 0) & (vars['dir']['FRTR'][j] < 0)):
                        comp_tension[i]['FRTR'][j] = 'compression'
                    elif ((vars[i]['FRTR'][j] < 0) & (vars['dir']['FRTR'][j] > 0)) | ((vars[i]['FRTR'][j] > 0) & (vars['dir']['FRTR'][j] < 0)):
                        comp_tension[i]['FRTR'][j] = 'tension'
                    else:
                        comp_tension[i]['FRTR'][j] = 'error'
                else:
                    # coil over case
                    comp_tension[i]['FRTR'][j] = 'error'
                    if ((vars[i]['FRCO'][j] > 0) & (vars['dir']['FRCO'][j] > 0)) | ((vars[i]['FRCO'][j] < 0) & (vars['dir']['FRCO'][j] < 0)):
                        comp_tension[i]['FRCO'][j] = 'compression'
                    elif ((vars[i]['FRCO'][j] < 0) & (vars['dir']['FRCO'][j] > 0)) | ((vars[i]['FRCO'][j] > 0) & (vars['dir']['FRCO'][j] < 0)):
                        comp_tension[i]['FRCO'][j] = 'tension'
                    else:
                        comp_tension[i]['FRCO'][j] = 'error'

        print("COMP TENSION: ", comp_tension['braking'])
                

        magnitude = {'braking': {'FRLF': None, 'FRLA': None, 'FRTR': None},
                    'cornering': {'FRLF': None, 'FRLA': None, 'FRTR': None}, 
                    'accel': {'FRLF': None, 'FRLA': None, 'FRTR': None}, 
                    'bump': {'FRLF': None, 'FRLA': None, 'FRTR': None},
                    'cornering and bump': {'FRLF': None, 'FRLA': None, 'FRTR': None},
                    'accel and bump': {'FRLF': None, 'FRLA': None, 'FRTR': None},
                    'braking and bump': {'FRLF': None, 'FRLA': None, 'FRTR': None}}

        # magnitude calcs
        for i in iterable_categories:
            if i == 'dir':
                continue
            if lower_upper == 'Lower':
                magnitude[i]['FRCO'] = 'error'
                for m in ['FRLF', 'FRLA', 'FRTR']:
                    if (vars[i][m]['X'] == 'error') | (vars[i][m]['Y'] == 'error') | (vars[i][m]['Z'] == 'error'):
                        magnitude[i][m] = 'error'
                    else:
                        magnitude[i][m] = np.sqrt(vars[i][m]['X']**2 + vars[i][m]['Y']**2 + vars[i][m]['Z']**2)
                        # magnitude[i][m] = np.sqrt(vars[i][m]['X']**2 + vars[i][m]['Y']**2 + vars[i][m]['Z']**2)
                        # magnitude[i][m] = np.sqrt(vars[i][m]['X']**2 + vars[i][m]['Y']**2 + vars[i][m]['Z']**2)
            else:
                magnitude[i]['FRTR'] = 'error'
                for m in ['FRLF', 'FRLA', 'FRCO']:
                    if (vars[i][m]['X'] == 'error') | (vars[i][m]['Y'] == 'error') | (vars[i][m]['Z'] == 'error'):
                        magnitude[i][m] = 'error'
                    else:
                        magnitude[i][m] = np.sqrt(vars[i][m]['X']**2 + vars[i][m]['Y']**2 + vars[i][m]['Z']**2)
                        # magnitude[i][m] = np.sqrt(vars[i][m]['X']**2 + vars[i][m]['Y']**2 + vars[i][m]['Z']**2)
                        # magnitude[i][m] = np.sqrt(vars[i][m]['X']**2 + vars[i][m]['Y']**2 + vars[i][m]['Z']**2)

        print()
        print("MAGNITUDE: ", magnitude)
        print()

        load_case = {'braking': {'FRLF': None, 'FRLA': None, 'FRTR': None},
                    'cornering': {'FRLF': None, 'FRLA': None, 'FRTR': None}, 
                    'accel': {'FRLF': None, 'FRLA': None, 'FRTR': None}, 
                    'bump': {'FRLF': None, 'FRLA': None, 'FRTR': None},
                    'cornering and bump': {'FRLF': None, 'FRLA': None, 'FRTR': None},
                    'accel and bump': {'FRLF': None, 'FRLA': None, 'FRTR': None},
                    'braking and bump': {'FRLF': None, 'FRLA': None, 'FRTR': None}}

        # load case calcs
        for i in iterable_categories:
            if i == 'dir':
                continue

            if lower_upper == 'Lower':
                load_case[i]['FRCO'] = 'error'
                for m in ['FRLF', 'FRLA', 'FRTR']:
                    if (comp_tension[i][m]['X'] == comp_tension[i][m]['Y']) & (comp_tension[i][m]['Y'] == comp_tension[i][m]['Z']):
                        load_case[i][m] = comp_tension[i][m]['X']
                    else:
                        load_case[i][m] = 'error'

            else:
                load_case[i]['FRTR'] = 'error'
                for m in ['FRLF', 'FRLA', 'FRCO']:
                    if (comp_tension[i][m]['X'] == comp_tension[i][m]['Y']) & (comp_tension[i][m]['Y'] == comp_tension[i][m]['Z']):
                        load_case[i][m] = comp_tension[i][m]['X']
                    else:
                        load_case[i][m] = 'error'


        print()
        print("LOAD CASE: ", load_case)
        print()

        min_I = {'braking': {'FRLF': None, 'FRLA': None, 'FRTR': None, 'FRCO': None},
                    'cornering': {'FRLF': None, 'FRLA': None, 'FRTR': None, 'FRCO': None}, 
                    'accel': {'FRLF': None, 'FRLA': None, 'FRTR': None, 'FRCO': None}, 
                    'bump': {'FRLF': None, 'FRLA': None, 'FRTR': None, 'FRCO': None},
                    'cornering and bump': {'FRLF': None, 'FRLA': None, 'FRTR': None, 'FRCO': None},
                    'accel and bump': {'FRLF': None, 'FRLA': None, 'FRTR': None, 'FRCO': None},
                    'braking and bump': {'FRLF': None, 'FRLA': None, 'FRTR': None, 'FRCO': None}
                }

        
        # min_I calcs
        # I = second moment of area
        all_min_I = {'FRLF': [], 'FRLA': [], 'FRTR': [], 'FRCO': []}
        for i in iterable_categories:
            if i == 'dir':
                continue

            # buckling only occurs during compression
            for m in ['FRLF', 'FRLA', 'FRTR', 'FRCO']:
                # IF(I7="Compression",(H7*(1*I2)^2)/((PI()^2)*Central!$P$4))
                if load_case[i][m] == 'compression':
                    try:
                        length_to_use = None
                        if m == 'FRLF':
                            length_to_use = length_frlf_in
                        elif m == 'FRLA':
                            length_to_use = length_frla_in
                        elif m == 'FRTR':
                            length_to_use = length_FRTR_in
                        else:
                            length_to_use = length_frco_in

                        min_I[i][m] = (magnitude[i][m]*((length_to_use)**2))/((np.pi**2)*elastic_modulus) # TODO: fix length
                        all_min_I[m].append((magnitude[i][m]*((length_to_use)**2))/((np.pi**2)*elastic_modulus))
                    except:
                        min_I[i][m] = 'error'
                else:
                    min_I[i][m] = None


        print()
        print('MIN I: ', min_I)
        print()

        min_area = {'braking': {'FRLF': None, 'FRLA': None, 'FRTR': None, 'FRCO': None},
                    'cornering': {'FRLF': None, 'FRLA': None, 'FRTR': None, 'FRCO': None}, 
                    'accel': {'FRLF': None, 'FRLA': None, 'FRTR': None, 'FRCO': None}, 
                    'bump': {'FRLF': None, 'FRLA': None, 'FRTR': None, 'FRCO': None},
                    'cornering and bump': {'FRLF': None, 'FRLA': None, 'FRTR': None, 'FRCO': None},
                    'accel and bump': {'FRLF': None, 'FRLA': None, 'FRTR': None, 'FRCO': None},
                    'braking and bump': {'FRLF': None, 'FRLA': None, 'FRTR': None, 'FRCO': None}
                    }

        all_min_area = {'FRLF': [], 'FRLA': [], 'FRTR': [], 'FRCO': []}
        # min_area calcs
        for i in iterable_categories:
            if i == 'dir':
                continue

            for m in ['FRLF', 'FRLA', 'FRTR', 'FRCO']:
                if load_case[i][m] == 'tension':
                    try:
                        min_area[i][m] = magnitude[i][m]/tensile_yield
                        all_min_area[m].append(magnitude[i][m]/tensile_yield)
                    except:
                        # should never reach this case
                        min_area[i][m] = 'error'
                else:
                    min_area[i][m] = None

        print()
        print("MIN AREA: ", min_area)
        print()
        # MAIN RESULTS CALCULATIONS
        main_results = {'FRLF': {'min_I': None, 'min_area': None, 
                                'r1': None, 'r2': None, 'I (from r1 r2)': None,
                                'I': None,
                                'FoS (I)': None, 'Area': None, 'FoS (A)': None,
                                'Weight': None},
                        'FRLA': {'min_I': None, 'min_area': None, 
                                'r1': None, 'r2': None, 'I (from r1 r2)': None,
                                'I': None,
                                'FoS (I)': None, 'Area': None, 'FoS (A)': None,
                                'Weight': None},
                        'FRTR': {'min_I': None, 'min_area': None, 
                                'r1': None, 'r2': None, 'I (from r1 r2)': None,
                                'I': None,
                                'FoS (I)': None, 'Area': None, 'FoS (A)': None,
                                'Weight': None},
                        'FRCO': {'min_I': None, 'min_area': None, 
                                'r1': None, 'r2': None, 'I (from r1 r2)': None,
                                'I': None,
                                'FoS (I)': None, 'Area': None, 'FoS (A)': None,
                                'Weight': None}
                        }


        for i in ['FRLF', 'FRLA', 'FRTR', 'FRCO']:
            
            try:
                main_results[i]['min_I'] = max(all_min_I[i])
            except:
                main_results[i]['min_I'] = None
            try:
                main_results[i]['min_area'] = max(all_min_area[i])
            except:
                main_results[i]['min_area'] = None

            main_results[i]['r1'] = tube_diameters[i]/2 # radius of tube
            main_results[i]['r2'] = main_results[i]['r1'] - tube_thicknesses[i]
            main_results[i]['I (from r1 r2)'] = (np.pi/4)*(main_results[i]['r1']**4 - main_results[i]['r2']**4)
            main_results[i]['I'] = np.pi*((tube_diameters[i]**4 - (tube_diameters[i] - 2*tube_thicknesses[i])**4)/64)
            try:
                main_results[i]['FoS (I)'] = main_results[i]['I']/main_results[i]['min_I'] # could be error
                # if main_results[i]['FoS (I)'] < 1:
                #     # find and print the case
                #     print("-------------------")
                #     print()
                #     print(vars)
                #     print()
                #     print(min_I)
                #     print()
                #     print(min_area)
                #     print()
                #     print("--------------------")
            except:
                main_results[i]['FoS (I)'] = 'error'

            main_results[i]['Area'] = np.pi*((tube_diameters[i]/2)**2 - ((tube_diameters[i]/2) - tube_thicknesses[i])**2)

            try:
                main_results[i]['FoS (A)'] = main_results[i]['Area']/main_results[i]['min_area'] # could be error
            except:
                main_results[i]['FoS (A)'] = 'error'

            main_results[i]['Weight'] = main_results[i]['Area']*tube_thicknesses[i]*0.284

        print()
        print("MAIN RESULTS: ", main_results)
        print()
        # display results table
        createResultsFrame(main_results['FRLF'], main_results['FRLA'], main_results['FRTR'], main_results['FRCO'])
        



    """
    Defining the GUI
    """
    root = Tk()
    frm = ttk.Frame(root, padding=100)
    root.title("Control Arm Sizing")
    frm.grid()
    # ttk.Label(frm, text="Control Arm Sizing").grid(column=0, row=0)
    # add user input stuff

    ttk.Button(frm, text="FLU", command=lambda: updateCurrentCorner("FLU")).grid(column=0, row=0)
    ttk.Button(frm, text="FLL", command=lambda: updateCurrentCorner("FLL")).grid(column=1, row=0)
    ttk.Button(frm, text="FRU", command=lambda: updateCurrentCorner("FRU")).grid(column=2, row=0)
    ttk.Button(frm, text="FRL", command=lambda: updateCurrentCorner("FRL")).grid(column=3, row=0)
    ttk.Button(frm, text="RLU", command=lambda: updateCurrentCorner("RLU")).grid(column=4, row=0)
    ttk.Button(frm, text="RLL", command=lambda: updateCurrentCorner("RLL")).grid(column=5, row=0)
    ttk.Button(frm, text="RRU", command=lambda: updateCurrentCorner("RRU")).grid(column=6, row=0)
    ttk.Button(frm, text="RRL", command=lambda: updateCurrentCorner("RRL")).grid(column=7, row=0)


    ttk.Label(frm, text="Fore").grid(column=1, row=1)
    ttk.Label(frm, text="Aft").grid(column=2, row=1)
    ttk.Label(frm, text="Tie Rod").grid(column=3, row=1)
    ttk.Label(frm, text="PR").grid(column=4, row=1)

    ttk.Label(frm, text="Tube Diameter Inputs: ").grid(column=0, row=2)
    ttk.Label(frm, text="Tube Thickness Inputs: ").grid(column=0, row=3)

    ttk.Label(frm, text="Add Data: ").grid(column=0, row=4)

    tubeDiameterEntry_FRLF_var = tk.StringVar()
    tubeDiameterEntry_FRLA_var = tk.StringVar()
    tubeDiameterEntry_FRTR_var = tk.StringVar()
    tubeDiameterEntry_FRCO_var = tk.StringVar()

    tubeThicknessEntry_FRLF_var = tk.StringVar()
    tubeThicknessEntry_FRLA_var = tk.StringVar()
    tubeThicknessEntry_FRTR_var = tk.StringVar()
    tubeThicknessEntry_FRCO_var = tk.StringVar()

    tubeDiameterEntry_FRLF_entry = ttk.Entry(frm, textvariable=tubeDiameterEntry_FRLF_var).grid(column = 1, row = 2)
    tubeDiameterEntry_FRLA_entry = ttk.Entry(frm, textvariable=tubeDiameterEntry_FRLA_var).grid(column = 2, row = 2)
    tubeDiameterEntry_FRTR_entry = ttk.Entry(frm, textvariable=tubeDiameterEntry_FRTR_var).grid(column = 3, row = 2)
    tubeDiameterEntry_FRCO_entry = ttk.Entry(frm, textvariable=tubeDiameterEntry_FRCO_var).grid(column = 4, row = 2)

    tubeDiameterEntry_FRLF_var.trace_add("write", updateInputVars)
    tubeDiameterEntry_FRLA_var.trace_add("write", updateInputVars)
    tubeDiameterEntry_FRTR_var.trace_add("write", updateInputVars)
    tubeDiameterEntry_FRCO_var.trace_add("write", updateInputVars)

    tubeThicknessEntry_FRLF_entry = ttk.Entry(frm, textvariable=tubeThicknessEntry_FRLF_var).grid(column = 1, row = 3)
    tubeThicknessEntry_FRLA_entry = ttk.Entry(frm, textvariable=tubeThicknessEntry_FRLA_var).grid(column = 2, row = 3)
    tubeThicknessEntry_FRTR_entry = ttk.Entry(frm, textvariable=tubeThicknessEntry_FRTR_var).grid(column = 3, row = 3)
    tubeThicknessEntry_FRCO_entry = ttk.Entry(frm, textvariable=tubeThicknessEntry_FRCO_var).grid(column = 4, row = 3)

    tubeThicknessEntry_FRLF_var.trace_add("write", updateInputVars)
    tubeThicknessEntry_FRLA_var.trace_add("write", updateInputVars)
    tubeThicknessEntry_FRTR_var.trace_add("write", updateInputVars)
    tubeThicknessEntry_FRCO_var.trace_add("write", updateInputVars)



    # add data buttons
    ttk.Button(frm, text="Direction Data", command=directionUploadAction).grid(column=1, row=4)
    ttk.Button(frm, text="Braking Data", command=brakingUploadAction).grid(column=2, row=4)
    ttk.Button(frm, text="Cornering Data", command=corneringUploadAction).grid(column=3, row=4)
    ttk.Button(frm, text="Accel Data", command=accelUploadAction).grid(column=4, row=4)
    ttk.Button(frm, text="Bump Data", command=bumpUploadAction).grid(column=5, row=4)
    ttk.Button(frm, text="Run Calculations", command=RunApp).grid(column=0, row=5)



    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=0, row=6)
    root.mainloop()


if __name__ == '__main__':
    main()