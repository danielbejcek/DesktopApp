import pandas as pd
pd.options.display.width= None
pd.options.display.max_columns= None
pd.set_option('display.max_rows', 5000)
pd.set_option('display.max_columns', 3000)


components = {"Komponent":
                ["NOHA ALU 25",
                 "NOHA ALU 12",
                 "PANT ALU ALFA „P“",
                 "PANT ALU ALFA „L“",
                 "PANT ALU AQUA/NERO „P“",
                 "PANT ALU AQUA/NERO „L“",
                 "KLIKA PŮLKULATÁ",
                 "KNOBKA",
                 "OTOČNÝ NEREZ",
                 "ZADLABÁVACÍ „P“",
                 "ZADLABÁVACÍ „L“",
                 "HÁČKY ALU",
                 "HÁČKY NEREZ",
                 "NOHA NEREZ 25",
                 "NOHA NEREZ 12",
                 "PANT NEREZ ALFA „P“",
                 "PANT NEREZ ALFA „L“",
                 "PANT NEREZ AQUA/NERO „P“",
                 "PANT NEREZ AQUA/NERO „L“",
                 "VINGL ALU",
                 "DORAZ PLAST",
                 "PANT NAT. ALU ALFA „P“",
                 "PANT NAT. ALU ALFA „L“",
                 "PANT NAT. ALU NERO „P“",
                 "PANT NAT. ALU NERO „L“",
                 "PANT NAT. NEREZ ALFA „P“",
                 "PANT NAT. NEREZ ALFA „L“",
                 "PANT NAT. NEREZ NERO „P“",
                 "PANT NAT. NEREZ NERO „L“",
                 "ZADLABÁVACÍ FAB „P“",
                 "ZADLABÁVACÍ FAB „L“",
                 "KLIKA  HRANATÁ",
                 "KLIKA  FAB PŮLKULATÁ",
                 "KLIKA  FAB HRANATÁ",
                 "VIGL NEREZ",
                 "VĚŠÁK NEREZ",
                 ",,U,, PROFIL 25",
                 ",,U,, PROFIL 12"],

              "Množství":
                [0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0]}


old_df = pd.DataFrame(components)
df = pd.DataFrame(components)
# df.loc[df["Komponent"] == "NOHA ALU 25", "Množství"] = 25
df.at[5, 'Množství'] = 25
df.at[0, 'Množství'] = 30

# print(df)

