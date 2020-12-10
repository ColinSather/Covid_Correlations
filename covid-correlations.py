import matplotlib.pyplot as plt
import pandas as pd
import numpy as npy
import sys, math

# uninstall scipy
class covid_correlations:
    def __init__(self, df):
        self.df = df

    def onpick3(self, event):
        ind = event.ind
        ind = ind[0]
        print('\nSelected County:', df["county"][ind])
        print('Covid Cases:', df["cases"][ind])
        print('Population:', df["population"][ind])
        print("NR Value:", df["nr sum"][ind])

    def create_plot(self):
        fig, ax1 = plt.subplots()
        ax1.plot(df["cases"], df["population"], 'bo', label="California Counties", picker=True)
        plt.xlabel("COVID-19 Cases")
        plt.ylabel("County Population")
        plt.legend(loc="upper left")
        fig.canvas.mpl_connect('pick_event', self.onpick3)
        plt.show()
    
    def multi_correlation(self):
        # Get pairwise correlation coefficients
        cor = df.corr()

        # Independent variables
        x = 'population'
        y = 'nr sum'

        # Dependent variable
        z = 'cases'

        # pairwise correlations
        xz = cor.loc[x, z]
        yz = cor.loc[y, z]
        xy = cor.loc[x, y]

        Rxyz = math.sqrt((abs(xz**2) + abs(yz**2) - 2*xz*yz*xy) / (1-abs(xy**2)) )
        R2 = Rxyz**2

        # Calculate adjusted R-squared
        n = len(df) # Number of rows
        k = 2       # Number of independent variables
        R2_adj = 1 - ( ((1-R2)*(n-1)) / (n-k-1) )

        return R2, R2_adj


if __name__ == "__main__":
    df = pd.read_csv("data/RawData.csv")
    cc_obj = covid_correlations(df)
    
    try:    
        if sys.argv[1] == str(1):
            # launch matplot lib gui
            cc_obj.create_plot()

        if sys.argv[1] == str(2):
            ret = cc_obj.multi_correlation()
            print(ret)
    
    except:
        print("Error: Did you provide a command line argument? Type either type 1 or 2 allong with the script execution.")