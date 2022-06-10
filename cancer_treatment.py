import streamlit as st
import numpy as np
import altair as alt
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import math
import random
import pandas as pd

## Main streamlit page
st.title("Adaptive Therapy Simulation: Cancer Treatment and Resistance")
st.write("Think Tank Matematicas 2022")
st.write()
st.sidebar.write('Hello! In this project, we are simulating our ODE model for populations of sensitive and resistance cell in adaptive therapy.')
st.sidebar.write("Our Models:")
st.sidebar.latex(r'''
    \dot{x} = 1.2x(1-\frac{x+y}{k}) - d(t)x
''')
st.sidebar.latex(r'''
    \dot{y} = 0.8y(1 - \frac{x+y}{k}) - 0.5y
''')
d_rate = st.sidebar.slider(
    'Select the value of death rate d:',
    0.0, 0.01, 5.0
)
k = st.sidebar.slider(
    'Select the value of carrying capacity k:',
    100, 1, 1000
)
time = st.sidebar.slider(
    'Select the maximum treatment time:',
    1.00, 0.01, 5.00
)
st.sidebar.latex(r'''
    x = \text{ Sensitive cell population}\\
    y = \text{ Resistant cell population}\\
    r_2 > r_1 > 0 = \text{ Growth rate of cells}\\
    d_1(t) > 0.5 = \text{ Death reate of sensitive cells}\\
    k = \text{ Carrying capacity}
''')
st.sidebar.write('What is Adaptive Therapy? - Adaptive therapy is a type of cancer treatment that aims to maintain sesntive cell populations to limit resistant cell growth. Treatment features decreasing does over time and increasing efficacy of larger drug doeses at later time points.')

## Adaptive therapy 1
z0 = [100, 10]
timeElapsed = 0
# Create an empty dataframe
df1 = pd.DataFrame(columns = ['time', 'sensitive_cells', 'resistant_cells'])
# Simulation
for x in range(1, 200):
    if ((z0[0] + z0[1]) >= 0.2*110):
        a = d_rate #Choose a such that 0 < d2/r2 < d1/r1 and d2/r2<1
    if (z0[0] + z0[1]) < 110 or (z0[1] > 50):
        a = .5 #Choose a such that 0 < d1/r1 < d2/r2 and d1/r1<1
    def treat(z, t):
        x, y = z
        dzdt = [1.2*x*(1-(x+y)/k)-(a)*x, 0.8*y*(1-(x+y)/k)-.5*y]
        return dzdt

    #if x == 1:
        #z0 = [100, 10] #inital pop of sus, res cells 
    if x > 1:
        z0 = [sol[100, 0], sol[100, 1]] 
    
    randomTime = time*random.random() + .001#random.random(0.1,3)
    t = np.linspace(timeElapsed, timeElapsed + randomTime, 101) #t = np.linspace(.1*(x-1), .1*x, 101)
    sol = odeint(treat, z0, t)
    timeElapsed = timeElapsed + randomTime

    df1_new = pd.DataFrame(sol, columns = ['sensitive_cells', 'resistant_cells'])
    df1_new.insert(loc = 0, column = "time", value = timeElapsed)
    df1 = df1.append(df1_new)
df1['total_pop'] = df1['sensitive_cells'] + df1['resistant_cells']
## Creating plots
plot1_1 = alt.Chart(df1).mark_circle(size = 30).encode(
    x = alt.X("time", title = "Time"),
    y = alt.Y("sensitive_cells", scale = alt.Scale(domain=[0,1000]), title = "Population of Cells"),
    color = alt.value("#145DA0"),
    tooltip = ["time","sensitive_cells"]
).interactive()
# plot for population of resistant cells
plot2_1 = alt.Chart(df1).mark_circle(size = 30).encode(
    x = alt.X("time", title = "Time"),
    y = alt.Y("resistant_cells", scale = alt.Scale(domain=[0,1000]),title = "Population of Cells"),
    color = alt.value("#8E1600"),
    tooltip = ["time","resistant_cells"]
).interactive()
# plot for total population
plot3_1 = alt.Chart(df1).mark_circle(size = 30).encode(
    x = alt.X("time", title = "Time"),
    y = alt.Y("total_pop", scale = alt.Scale(domain=[0,1000]),title = "Population of Cells"),
    color = alt.value("#234F1E"),
    tooltip = ["time","resistant_cells"]
).interactive()
# plot combining both plot1 and plot2
plot3_1 = alt.layer(
    plot1_1.mark_line(), 
    plot2_1.mark_line(),
    plot3_1.mark_line(),
)

## Adaptive Therapy 2
z0 = [100, 10]
timeElapsed = 0
# Empty dataframe
df2 = pd.DataFrame(columns = ['time', 'sensitive_cells', 'resistant_cells'])
# Simulation
for x in range(1, 100):
    if z0[0] <= z0[1]:
        a = 0.5 # stop treatment
    elif z0[0] > z0[1]:
        a = d_rate # start treatment
    if x > 1:
        z0 = [sol[100, 0], sol[100, 1]] 
    def treat(z, t):
        x, y = z
        dzdt = [1.2*x*(1-(x+y)/k)-a*x, 0.8*y*(1-(x+y)/k)-.5*y]
        return dzdt
    randomTime = time*random.random() + .001#random.random(0.1,3)
    t = np.linspace(timeElapsed, timeElapsed + randomTime, 101) #t = np.linspace(.1*(x-1), .1*x, 101)
    sol = odeint(treat, z0, t)
    timeElapsed = timeElapsed + randomTime

    df2_new = pd.DataFrame(sol, columns = ['sensitive_cells', 'resistant_cells'])
    df2_new.insert(loc = 0, column = "time", value = timeElapsed)
    df2 = df2.append(df2_new)
df2['total_pop'] = df2['sensitive_cells'] + df2['resistant_cells']
## Creating plots
plot1_2 = alt.Chart(df2).mark_circle(size = 30).encode(
    x = alt.X("time", title = "Time"),
    y = alt.Y("sensitive_cells", scale = alt.Scale(domain=[0,1000]), title = "Population of Cells"),
    color = alt.value("#145DA0"),
    tooltip = ["time","sensitive_cells"]
).interactive()
# plot for population of resistant cells
plot2_2 = alt.Chart(df2).mark_circle(size = 30).encode(
    x = alt.X("time", title = "Time"),
    y = alt.Y("resistant_cells", scale = alt.Scale(domain=[0,1000]),title = "Population of Cells"),
    color = alt.value("#8E1600"),
    tooltip = ["time","resistant_cells"]
).interactive()
# plot for total population
plot3_2 = alt.Chart(df2).mark_circle(size = 30).encode(
    x = alt.X("time", title = "Time"),
    y = alt.Y("total_pop", scale = alt.Scale(domain=[0,1000]),title = "Population of Cells"),
    color = alt.value("#234F1E"),
    tooltip = ["time","resistant_cells"]
).interactive()
# plot combining both plot1 and plot2
plot3_2 = alt.layer(
    plot1_2.mark_line(), 
    plot2_2.mark_line(),
    plot3_2.mark_line(),
)


# Adaptive Therapy 3
z0 = [100, 10]
timeElapsed = 0
#empty dataframe
df3 = pd.DataFrame(columns = ['time', 'sensitive_cells', 'resistant_cells'])
for x in range(1, 1000):
    if z0[0] <= z0[1]:
        def treat(z, t):
            x, y = z
            dzdt = [1.2*x*(1-(x+y)/k)-0.5*x, 0.8*y*(1-(x+y)/k)-.5*y]
            return dzdt
    elif z0[0] > z0[1]:
        def treat(z, t):
            x, y = z
            dzdt = [1.2*x*(1-(x+y)/k)-((t-timeElapsed+d_rate)**2)*x, 0.8*y*(1-(x+y)/k)-.5*y]
            return dzdt
    if x > 1:
        z0 = [sol[100, 0], sol[100, 1]] 
    randomTime = time*random.random() + .001#random.random(0.1,3)
    t = np.linspace(timeElapsed, timeElapsed + randomTime, 101) #t = np.linspace(.1*(x-1), .1*x, 101)
    sol = odeint(treat, z0, t)
    timeElapsed = timeElapsed + randomTime
    df3_new = pd.DataFrame(sol, columns = ['sensitive_cells', 'resistant_cells'])
    df3_new.insert(loc = 0, column = "time", value = timeElapsed)
    df3 = df3.append(df3_new)
df3['total_pop'] = df3['sensitive_cells'] + df3['resistant_cells']
## Creating plots
plot1_3 = alt.Chart(df3).mark_circle(size = 30).encode(
    x = alt.X("time", title = "Time"),
    y = alt.Y("sensitive_cells", scale = alt.Scale(domain=[0,1000]), title = "Population of Cells"),
    color = alt.value("#145DA0"),
    tooltip = ["time","sensitive_cells"]
).interactive()
# plot for population of resistant cells
plot2_3 = alt.Chart(df3).mark_circle(size = 30).encode(
    x = alt.X("time", title = "Time"),
    y = alt.Y("resistant_cells", scale = alt.Scale(domain=[0,1000]),title = "Population of Cells"),
    color = alt.value("#8E1600"),
    tooltip = ["time","resistant_cells"]
).interactive()
# plot for total population
plot3_3 = alt.Chart(df3).mark_circle(size = 30).encode(
    x = alt.X("time", title = "Time"),
    y = alt.Y("total_pop", scale = alt.Scale(domain=[0,1000]),title = "Population of Cells"),
    color = alt.value("#234F1E"),
    tooltip = ["time","resistant_cells"]
).interactive()
# plot combining both plot1 and plot2
plot3_3 = alt.layer(
    plot1_3.mark_line(), 
    plot2_3.mark_line(),
    plot3_3.mark_line(),
)

st.write("Adaptive Therapy 1: ")
st.latex(r'''
    \text{Let } N(t) = x(t) + y(t)\\
''')
st.latex(r'''
    d(t) = 
    \begin{cases}
        d,& \text{if } N(t) \geq 20\%110\\
        0.5,              & \text{if } N(t) < 110 \text{ or } y(t) > 50
    \end{cases} 
''')
st.altair_chart(plot3_1, use_container_width=True)
st.write("Adaptive Therapy 2: ")
st.latex(r'''
    d(t) = 
    \begin{cases}
        d,& \text{if } x(t) > y(t) \\
        0.5,             & \text{if } x(t) \leq y(t)
    \end{cases} 
''')
st.altair_chart(plot3_2, use_container_width=True)
st.write("Adaptive Therapy 3: ")
st.latex(r'''
    d(t) = 
    \begin{cases}
        (t+d)^2,& \text{if } x(t) \geq y(t) \\
        0.5,             & \text{if } x(t) < y(t)
    \end{cases} 
''')
st.altair_chart(plot3_3, use_container_width=True)
