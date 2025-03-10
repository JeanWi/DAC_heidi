import adopt_net0 as adopt
import json
from pathlib import Path
import pandas as pd

data = {"Chile2030": {"p_heat": 126, "p_el": 100, "climate_data_sheet": "Chile_Data"},
        "Chile2050": {"p_heat": 126, "p_el": 100, "climate_data_sheet": "Chile_Data"},
        "Switzerland2030": {"p_heat": 27, "p_el": 70, "climate_data_sheet": "Switzerland_Data"},
        "Switzerland2050": {"p_heat": 27, "p_el": 16.8, "climate_data_sheet": "Switzerland_Data"}}

input_data_path = Path("./caseStudies/dac")


for case in data.keys():
    print(case)
    climate_data = pd.read_excel(Path("./caseStudies/data/Template_DACInvest_filled_HEIDI.xlsx"), sheet_name=data[case]["climate_data_sheet"], skiprows=3)
    T = climate_data["temperature_2m (¬∞C)"][0:8760].to_list()
    RH = climate_data["relative_humidity_2m (%)"][0:8760].to_list()

    adopt.fill_carrier_data(input_data_path, value_or_data=data[case]["p_el"], columns=['Import price'], carriers=['electricity'], nodes=["n1"])
    adopt.fill_carrier_data(input_data_path, value_or_data=data[case]["p_heat"], columns=['Import price'], carriers=['heat'], nodes=["n1"])

    cd = pd.read_csv(input_data_path / "period1" / "node_data" / "n1" / "ClimateData.csv", sep=";", index_col=0)

    cd.loc[:, "rh"] = RH
    cd.loc[:, "temp_air"] = T

    cd.to_csv(input_data_path / "period1" / "node_data" / "n1" / "ClimateData.csv", sep=";")

    m = adopt.ModelHub()
    m.read_data(input_data_path, start_period=0, end_period=1)
    m.quick_solve()


