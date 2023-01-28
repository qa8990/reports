from pyjavaproperties import Properties
import pandas as pd


def read_properties_file(file_path):
    p = Properties()
    p.load(open(file_path))
    #p.list()
    #print(p)
    return p

def read_master_plan():
    # Read the stock data file
    print("view master plan")
    master_plan_df = pd.read_csv('apps/static/assets/data/PLANDECUENTAS.csv', delimiter=',', header=0)
    print(master_plan_df, type(master_plan_df))
    return master_plan_df