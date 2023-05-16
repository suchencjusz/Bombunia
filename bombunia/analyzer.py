import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import numpy
import io
import base64

# from PIL import Image
import PIL

from tabulate import tabulate


class Analyzer:
    
    # def graph_from_list_by_subject(self, l):


    def graph_from_list(self, l):
        _valid = []

        for i in l:
            if i != -1:
                _valid.append(i)

        _grades = []

        for i in _valid:

            if i[0]["sum_of_all_grades"] / i[0]["count_of_all_grades"] <= 0:
                continue

            x = {
                "date": i[0]["time"],
                "average": i[0]["sum_of_all_grades"] / i[0]["count_of_all_grades"],
            }
            _grades.append(x)

        df = pd.DataFrame(_grades)

        df["date"] = pd.to_datetime(df["date"], unit="s")

        # print(tabulate(df, headers="keys", tablefmt="psql"))

        sns.set_style("ticks")

        # plt.xticks(rotation=90)
        # plt.xticks(rotation=45, ha="right")
        

        # plt.title("Średnia ocen w czasie")
        # plt.xlabel("Data")
        # plt.ylabel("Średnia ocen")

        fig, ax = plt.subplots()
        sns.lineplot(data=df, x="date", y="average", ax=ax)

        plt.xticks(rotation=30, ha="right")
        
        fig.canvas.draw()

        return PIL.Image.frombytes('RGB', fig.canvas.get_width_height(),fig.canvas.tostring_rgb())

    def pie_differences_summary(self, l) -> PIL.Image:
        _summed_grades = [0, 0, 0, 0, 0, 0]
        _labels = []
        _colors = []

        for i in l:
            for idx, j in enumerate(i["grades"]):
                _summed_grades[idx] += j

        l = []

        _colors_setting = {
            0: "#d44040",
            1: "#ff774d",
            2: "#ffb940",
            3: "#a0c331",
            4: "#4cb050",
            5: "#3dbbf5",
        }

        for idx, i in enumerate(_summed_grades):
            if i > 0:
                _labels.append(f"{idx+1} -> {_summed_grades[idx]}")
                _colors.append(_colors_setting[idx])
                l.append(i)

        fig, ax = plt.subplots()
        ax.pie(l, labels=_labels, autopct="%1.1f%%", startangle=90, colors=_colors)
        
        fig.canvas.draw()

        return PIL.Image.frombytes('RGB', fig.canvas.get_width_height(),fig.canvas.tostring_rgb())

        


    # heat map of grades in poniedzialek - piatek model
