import pandas as pd
import numpy as np
from scipy.io import loadmat
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from datetime import datetime, date, time
import plotly.express as px
from scipy.optimize import curve_fit
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# helper functions
def kpa_to_psi(value):
    psi = value / 6.89475729
    return psi

# need user to give us their data file in .mat or csv format
def load_data(path_to_data):
    if '.mat' in path_to_data:
        # this is a matlab file => need to do preprocessing
        # to convert this to a dataframe
        mat = loadmat(path_to_data)
        cols = mat.keys()
        values = mat.values()

        # determine what vars to keep (default = all)
        target_keys = ['AMBTMP', 'ET', 'FX', 'FY', 'FZ', 'IA', 'MX', 'MZ', 'N', 'NFX', 'NFY', 'P', 'RE',
               'RL', 'RST', 'RUN', 'SA', 'SL', 'SR', 'TSTC', 'TSTI', 'TSTO', 'V']
        new_mat = {key: mat[key] for key in target_keys}

        # need to flatten our data because it's in difficult formatting
        new_mat_again = {}
        for col in new_mat.keys():
            ll = new_mat[col]
            flat = [val for sublist in ll for val in sublist]
            new_mat_again[col] = flat

        df = pd.DataFrame(new_mat_again)

        # converting slip angle to radians
        df['SA_rad'] = df['SA']*(np.pi/180)
        # convert kPa to psi
        df['P_psi'] = df.apply(lambda x: kpa_to_psi(x['P']), axis=1)

        return df

    elif '.csv' in path_to_data:
        # just a csv file
        df = pd.read_csv(path_to_data, encoding='ISO-8859-1')
        df['SA_rad'] = df['SA']*(np.pi/180)
        df['P_psi'] = df.apply(lambda x: kpa_to_psi(x['P']), axis=1)
        return df
    else:
        # throw an error and stop execution
        raise Exception("File format not supported")

def crop_data(df, criteria):
    # criteria format = COLUMN_NAME > SOME VALUE
    col_name = criteria.split()[0]
    crit_operator = criteria.split()[1]
    crit_value = float(criteria.split()[2]) # TODO: alter to have strings?

    # horribly repetitive, definitely a better way to do this
    if crit_operator == '>':
        df = df[df[col_name] > crit_value]
        return df
    elif crit_operator == '>=':
        df = df[df[col_name] >= crit_value]
        return df
    elif (crit_operator == '==') | (crit_operator == '='):
        df = df[df[col_name] == crit_value]
        return df
    elif (crit_operator == '!='):
        df = df[df[col_name] != crit_value]
        return df
    elif crit_operator == '<':
        df = df[df[col_name] < crit_value]
        return df
    elif crit_operator == '<=':
        df = df[df[col_name] <= crit_value]
        return df
    else:
        raise Exception("Criteria operator not accepted")

# DETERMINING THE MODEL
# option for custom model entirely input by user
# option for default model = simplest Pacejka possible
# some more prebuilt models that get thrown around the internet...

"""
MODEL SPECIFICATIONS
If you want to add a new model, create a new function (e.g., def new_model(...))
Then curve fit with the new model
"""

def basic_model(x, B, C, D, E):
     # from RCVD
     # x = slip angle
    return (D*np.sin(C*np.arctan(B*x - E*(B*x - np.arctan(B*x)))))

def pacejka_basic_model(x, B, C, D, E):
    # x = corresponding slip angle
    # y = Fx or Fy (or possibly Mz)
    # from Tyre and Vehicle Dynamics - Pacejka
    y = (D*np.sin(C*np.arctan(B*x - E*(B*x - np.arctan(B*x)))))
    return y

def pacejka_basic_extended(X, B, C, D, E):
    # x = slip angle
    # y = Fz
    slip, fz = X
    fz = -abs(fz)
    z = (fz*D*np.sin(C*np.arctan(B*slip - E*(B*slip - np.arctan(B*slip)))))
    return z

def pacejka4(X, d1, d2, b, c, sv, sh):
    # from some guy named cibachrome on reddit
    # don't worry
    # he says he knows his stuff, so it must be true
    slip, fz = X
    fz = -abs(fz) # fz is always negative
    d = (d1 + d2/1000*fz)*fz # normalizing peak value
    Fy = d*np.sin(c*np.arctan(b*(slip - sh))) + sv
    return Fy


def graph_model_2d(x, y, y_pred, xtext_label="x-axis", ytext_label="y_axis"):
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{'type': 'scatter'}, {'type': 'scatter'}]]
    )

    # the real data
    fig.add_trace(go.Scatter(x=x, y=y, name='Data'), row=1, col=1)

    # experimental data
    fig.add_trace(go.Scatter(x=x, y=y_pred, name='Predicted Data'), row=1, col=2)

    fig.update_layout(
        scene=dict(
            xaxis_title=xtext_label,
            yaxis_title=ytext_label
        )
    )

    fig.show()

def graph_model_3d(x, y, z, z_pred, xtext_label='x-axis', ytext_label='y-axis', ztext_label='z_axis'):
    xi = np.linspace(min(x), max(x), 100)
    yi = np.linspace(min(y), max(y), 100)
    X,Y = np.meshgrid(xi, yi)
    Z = griddata((x,y), z, (X, Y), method='cubic') # I think this is giving us the wrong data for surface plot

    fig = go.Figure()
    real_data = go.Scatter3d(x=x, y=y, z=z, mode='markers',
                            marker=dict(
                                size=5,
                                color='blue',
                                opacity=0.6
                            ), name='Real Data')
    model_prediction = go.Scatter3d(x=x, y=y, z=z_pred, mode='markers',
                            marker=dict(
                                size=5,
                                color='orange',
                                opacity=0.2
                            ), name='Model Prediction')
    fig.add_trace(real_data)
    fig.add_trace(model_prediction)

    fig.update_layout(
        title='3d Scatter Plot - Real vs Model Predictions',
    )
    fig.show()

    # WORKING for a surface plot through a 3d scatter plot but kinda weird so maybe wrong...
    # fig = go.Figure()
    # trace1 = go.Surface(x=xi, y=yi, z=Z, name='Surface')
    # trace2 = go.Scatter3d(x=x, y=y, z=z, mode='markers',
    #                 marker=dict(
    #                     size=5,
    #                     color=z,
    #                     colorscale='Viridis',
    #                     opacity=0.6
    #                 ), name='Data Points')

    # fig.add_trace(trace2)
    # fig.add_trace(trace1)

    # fig.show()

"""
EXAMPLE CODE - implementation
"""
df = load_data("./B2356run8.mat")
df = crop_data(df, 'ET > 900')
df = crop_data(df, 'ET < 1090')

# need user to define this
# FY MODEL
# note: for Fx model, change slip to be = np.array(df['SR'])
slip = np.array(df['SA'])
fz = np.array(df['FZ'])
X = (slip, fz)
fy = np.array(df['FY'])
popt, pcov = curve_fit(pacejka4, X, fy)

d1, d2, b, c, sv, sh = popt

# statistical scores
residuals = fy - pacejka4(X, d1, d2, b, c, sv, sh)
ss_res = np.sum(residuals**2)
ss_tot = np.sum((fy - np.mean(fy))**2)
r_squared = 1 - (ss_res/ss_tot)

print("Fy model")
print("Model R^2: ", r_squared)
print("d1: ", d1)
print("d2: ", d2)
print("b: ", b)
print("c: ", c)
print("sv: ", sv)
print("sh: ", sh)
print("-------------")

# uncomment to see graph of fit results
# graph_model_3d(slip, fz, fy, predicted_z)