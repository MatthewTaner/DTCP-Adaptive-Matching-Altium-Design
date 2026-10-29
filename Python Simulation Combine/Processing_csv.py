import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

RLoad = [25, 100, 300]
CLoad = [1e-11, 2e-11]
Freq = [9990100.0,14985100.0, 19980100.0, 24975100.0, 29970100.0] # there was error in n
Lload = np.arange(1, 9)
Lsource = np.arange(1,33)

NUM_FREQ = len(Freq)
NUM_LLOAD = len(Lload)
NUM_LSOURCE = len(Lsource)
NUM_RLOAD = len(RLoad)
NUM_CLOAD = len(CLoad)

# Steps change with frequeny first then Lload then Lsource

def get_number(i, array, num_steps_below):
    #Assuming i starts at 0
    position = int(int(i/num_steps_below) % len(array))
    return array[position]

df = pd.read_csv('Matching_sim_eff.csv', sep = r'\s+')
df1 = pd.read_csv('Matching_sim_Vmeas.csv', sep = r'\s+')
df2 = pd.read_csv('Matching_sim_pin.csv', sep = r'\s+')
df3 = pd.read_csv('Matching_sim_pout.csv', sep = r'\s+')
df.rename({"Idx":"Step","Col":"Efficiency"}, inplace=True, axis=1)
df1.rename({"Col":"Vmeas"}, inplace=True, axis=1)
df2.rename({"Col":"Pin"}, inplace=True, axis=1)
df3.rename({"Col":"Pout"}, inplace=True, axis=1)
CombinedDF = pd.concat([df, df1['Vmeas'], df2['Pin'], df3['Pout']], axis=1)
CombinedDF["Step"] = CombinedDF.index

CombinedDF["Freq"] = CombinedDF["Step"].apply(lambda n: get_number(n-1, Freq, 1))
CombinedDF = CombinedDF[CombinedDF["Freq"] > 7]
CombinedDF["Lload"] = CombinedDF["Step"].apply(lambda n: get_number(n-1, Lload, NUM_FREQ))
CombinedDF["Lsource"] = CombinedDF["Step"].apply(lambda n: get_number(n-1, Lsource, NUM_FREQ * NUM_LLOAD))
CombinedDF["RLoad"] = CombinedDF["Step"].apply(lambda n: get_number(n-1, RLoad, NUM_FREQ * NUM_LSOURCE * NUM_LLOAD))
CombinedDF["CLoad"] = CombinedDF["Step"].apply(lambda n: get_number(n-1, CLoad, NUM_FREQ * NUM_LSOURCE * NUM_LLOAD * NUM_RLOAD))
# Create a configuration column that combines the Lload and Lsource values and assigns a unique integer to each configuration
CombinedDF["Config"] = (CombinedDF["Lsource"]-1) + NUM_LSOURCE * (CombinedDF["Lload"]-1)
CombinedDF["dV/df"] = (CombinedDF.groupby('Config')["Vmeas"].diff() / CombinedDF.groupby('Config')["Freq"].diff()).fillna(0)
CombinedDF["Freq"] = CombinedDF["Freq"]/1e6



# Simulation2 Matching Effect of each inductor value
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
#ax.plot_surface(np.reshape(CombinedDF["Lload"], (3,5)), np.reshape(CombinedDF["Lsource"], (3,5)), np.reshape(CombinedDF["Efficiency"], (3, 5)))
sm = ax.scatter(CombinedDF["Lload"], CombinedDF["Lsource"], CombinedDF["Efficiency"], c = CombinedDF["Freq"], cmap='plasma')
plt.colorbar(sm, label='Frequency (MHz)')
ax.set_xlabel("Lload (nH)")
ax.set_ylabel("Lsource (nH)")
ax.set_zlabel("Efficiency")
ax.set_title("Efficiency vs Lload and Lsource")

# Measured voltage relationship with efficiency
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
#ax.plot_surface(np.reshape(CombinedDF["Lload"], (3,5)), np.reshape(CombinedDF["Lsource"], (3,5)), np.reshape(CombinedDF["Efficiency"], (3, 5)))
sm = ax.scatter(CombinedDF["Config"], CombinedDF["Vmeas"], CombinedDF["Efficiency"], c = CombinedDF["Freq"], cmap='plasma')
plt.colorbar(sm, label='Frequency (MHz)')
ax.set_xlabel("Configuration")
ax.set_ylabel("V measured (V)")
ax.set_zlabel("Efficiency")
ax.set_title("Efficiency vs Configuration and V measured (V)")


# Third Graph: Efficiency vs Pin
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
sm = ax.scatter(CombinedDF["Pin"], CombinedDF["Vmeas"], CombinedDF["Efficiency"], c = CombinedDF["Freq"], cmap='plasma')
plt.colorbar(sm, label='Frequency (MHz)')
ax.set_xlabel("Pin")
ax.set_ylabel("V measured (V)")
ax.set_zlabel("Efficiency")
ax.set_title("Efficiency vs Pin and V measured (V)")


# Fourth Graph:  Pout Efficiency V measured
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
sm = ax.scatter(CombinedDF["Pout"], CombinedDF["Vmeas"], CombinedDF["Efficiency"], c = CombinedDF["Freq"], cmap='plasma')
plt.colorbar(sm, label='Frequency (MHz)')
ax.set_xlabel("Pout")
ax.set_ylabel("V measured (V)")
ax.set_zlabel("Efficiency")
ax.set_title("Efficiency vs Pout and V measured (V)")

# Fifth Graph: Plot Efficiency vs Config's best Pout vs Pout
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
dfbest = CombinedDF.loc[CombinedDF.groupby(['Config'])["Pout"].idxmax()]
sm = ax.scatter(dfbest["Pout"], dfbest["Config"], dfbest["Efficiency"], c = dfbest["Freq"], cmap='plasma')
plt.colorbar(sm, label='Frequency (MHz)')
ax.set_xlabel("Pout")
ax.set_ylabel("Config")
ax.set_zlabel("Efficiency")
ax.set_title("Efficiency vs Pout and Config")

print(CombinedDF.iloc[np.argmax(CombinedDF["Pout"])])
print(CombinedDF[(CombinedDF["Lload"] == 1) & (CombinedDF["Lsource"] == 1)])
plt.show()