import numpy
import pandas as pd
import numpy as np


class UnclassifiedTable:
    def __init__(self, df):  # Imports and cleans up dataframe
        self.df = self.clean_table(df)

    def clean_table(self, df):
        '''
        Cleans up table to be better for analysis when object is initialized.
        :param df: dataframe that will be cleaned up
        :return: dataframe
        '''
        # Removes certain rows to clean up table
        if "SD" in df.index:
            df = df.drop("SD", axis='index')
        elif "Standard Deviation" in df.index:
            df = df.drop("Standard Deviation", axis='index')
        if "Variables" in df.index:
            df = df.drop("Variables", axis='index')
        if "Variable" in df.index:
            df = df.drop("Variable", axis='index')
        if "Mean" in df.index:
            df = df.drop("Mean", axis='index')
        if "Min." in df.index:
            df = df.drop("Min.", axis='index')
        if "Max." in df.index:
            df = df.drop("Min.", axis='index')

        # Removes certain columns to clean up table
        if "SD" in df.columns:
            df = df.drop("SD", axis='columns')
        elif "Standard Deviation" in df.columns:
            df = df.drop("Standard Deviation", axis='columns')
        if "Mean" in df.columns:
            df = df.drop("Mean", axis='columns')
        if "Variables" in df.columns:
            df = df.drop("Variables", axis='columns')
        if "Variable" in df.columns:
            df = df.drop("Variable", axis='columns')

        # Removes headers
        df = df.iloc[1:, 1:]

        # Removes symbol
        df = df.apply(lambda x: x.astype(str).str.replace("*", "", regex=True))
        df = df.apply(lambda x: x.astype(str).str.replace("-", "", regex=True))

        return df

    def compare_row_to_one(self, row) -> int:
        '''
        Counts amount of values greater than |1| in a row.
        Note, all - signs are removed in initalizaiton.
        :param row: row being analyzed
        :return: amount of values more than |1| in a row
        '''
        counter_more_than_one = 0

        for i in row:
            if i != "nan" and float(i) > 1:
                counter_more_than_one += 1

        return counter_more_than_one

    def classify_table(self) -> str:
        '''
        Attempts to identify if a table is correlation, regression, or other.
        Table is considered "other" if it its values is predominantly greater than 1.
        The reasoning is that correlation and regression relationships are logically <= 1.
        Table is considered "correlation" should it not be other AND it has a matrix shape.
        This essentially means that the amount of NaN decreases as you go down the row.
        Table is considered "regression" should it be not "other" or "correlation"
        :return: a string that identifies what type of table it is.
        '''
        df_array_NaN_amount = self.remove_zero_array(self.find_amount_NaN())
        amount_of_cell_greater_one = 0

        # Checks if table is "Other"
        for row in self.df.itertuples():
            amount_of_cell_greater_one = self.compare_row_to_one(row[1:])

        df_size = int(self.df.size)
        if amount_of_cell_greater_one > df_size / 4:
            return "other"

        # Classifies table as either regression or correlation
        threshold = len(df_array_NaN_amount) / 4  # If list of descending values is > than this, it is correl.
        list_descending_value = numpy.array([])

        if len(df_array_NaN_amount) > 0:
            for i in range(1, len(df_array_NaN_amount)):
                if df_array_NaN_amount[i] < df_array_NaN_amount[i - 1]:
                    list_descending_value = np.append(list_descending_value, df_array_NaN_amount[i])
                elif len(list_descending_value) <= threshold:
                    list_descending_value = numpy.array([])

        if len(list_descending_value) >= threshold:
            return "correlation"
        else:
            return ("regression")

    def remove_zero_array(self, input_array):
        # Removes all zeroes in array.
        return input_array[input_array != 0]

    def find_amount_NaN(self):
        '''
        Find the amount of NaN per row in an array.
        This information will be used to distinguish between a correlation and regression table.
        :return: a list of the amount of NaN per row in a dataframe.
        '''
        df_copy = self.df
        df_list_NaN_amount = np.array([])

        for i, row in df_copy.iterrows():
            df_copy.loc[i] = pd.to_numeric(df_copy.loc[i], errors='coerce', downcast='float')
            df_list_NaN_amount = np.append(df_list_NaN_amount, df_copy.loc[i].isna().sum())

        # Checks if table values are within |1| (they should be!)
        # self.dfCopy.apply(self.compare_cells_to_one)

        return df_list_NaN_amount
