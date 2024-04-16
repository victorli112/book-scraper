import pandas as pd

def combine_xlsx(output_file):
    # Load the Excel files
    xlsx1 = pd.ExcelFile("planeta/novela_contemporanea.xlsx")
    xlsx2 = pd.ExcelFile("planeta/novela_literaria.xlsx")
    xlsx3 = pd.ExcelFile("planeta/novela_negra.xlsx")
    xlsx4 = pd.ExcelFile("planeta/novelas_romanticas.xlsx")
    xlsx5 = pd.ExcelFile("planeta/poesia_historica.xlsx")

    # Get the sheet names
    sheet_names = xlsx1.sheet_names

    # Check if both documents have the same sheet names

    # Create a Pandas Excel writer using XlsxWriter as the engine
    writer = pd.ExcelWriter(output_file, engine='xlsxwriter')

    # Iterate over each sheet
    for sheet in sheet_names:
        df1 = pd.read_excel(xlsx1, sheet_name=sheet)
        df2 = pd.read_excel(xlsx2, sheet_name=sheet)
        df3 = pd.read_excel(xlsx3, sheet_name=sheet)
        df4 = pd.read_excel(xlsx4, sheet_name=sheet)
        df5 = pd.read_excel(xlsx5, sheet_name=sheet)

        # Print the initial number of rows
        print(f"Initial number of rows in '{sheet}': novela_contemporanea: {len(df1)} | novela_literaria: {len(df2)} | novela_negra: {len(df3)} | novelas_romanticas: {len(df4)} | poesia_historica: {len(df5)}")

        # Concatenate the dataframes
        df = pd.concat([df1, df2, df3, df4, df5])

        # Drop duplicates based on 'title' and 'author'
        df = df.drop_duplicates(subset=['Title', 'Author'])

        # Write each dataframe to a different worksheet
        df.to_excel(writer, sheet_name=sheet, index=False)

        # Print the final number of rows
        print(f"Final number of rows in '{sheet}' after combining: {len(df)}")

    # Close the Pandas Excel writer and output the Excel file
    writer.close()

combine_xlsx("planeta_books.xlsx")