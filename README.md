# Adaptive Therapy Simulation: Cancer Treatment and Development of Resistance

![](https://github.com/emicervantes/adaptive_therapy_simulation/sim-screenshot.png?raw=true)

This project focuses on building simulation website that enables user to see the optimized condition for adaptive therapy. Adaptive therapy is a type of cancer treatment that undergoes period of chemo therapy followed by "drug holiday", period of time when patients stop taking treatment. This type of treatment is effective in stabilizing the growth rate of tumor cell. We are using population growth ODE models for both susceptible/sensitive tumor cells and resistant tumor cells, with three different therapy conditions.

Simulation Link: https://emicervantes-adaptive-therapy-simulatio-cancer-treatment-nulkze.streamlit.app/

ODE Models: Let $\dot{x}$ denotes the population of susceptible tumor cells, and let $\dot{y}$ denotes the population of resistant tumor cells:

$$\dot{x} = r_1x(1-\frac{x+y}{k}) - d_1(t)x$$

$$\dot{x} = r_2y(1-\frac{x+y}{k}) - d_2(t)y$$

x = susceptible cell popuylation, y = resistant tumor cell population, $r_2>r_1>0$ = growth rate of cells (1 = susceptible cell, 2 = resistant cell), $d_1(t)>d_2>0$ = death rate of cell, k = carrying capacity

Therapy Conditions:Let $x(t) = 100$ and $y(t) = 10$ and Let $N(t)$ denote total population of cells such that $N(t) = x(t) + y(t)$

1. 

$$d(t) = 
      \begin{cases}
      d & \text{if $N(t) \geq 0.2*110$}\\
      0.5 & \text{if $N(t) < 110$ or $y(t) > 50$}\\
    \end{cases} $$
    
2. 

$$d(t) = 
      \begin{cases}
      d & \text{if $x(t) > y(t)$}\\
      0.5 & \text{if $x(t) \leq y(t)$}\\
    \end{cases} $$
    
3.

$$d(t) = 
      \begin{cases}
      (t+d)^2 & \text{if $x(t) \geq y(t)$}\\
      0.5 & \text{if $x(t) \leq y(t)$}\\
    \end{cases} $$

