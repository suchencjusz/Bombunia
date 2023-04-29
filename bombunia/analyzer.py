import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import io
import base64

from tabulate import tabulate


class Analyzer:
    def graph_from_list(self, l):
        _valid = []

        for i in l:
            if i != -1:
                _valid.append(i)

        _grades = []

        for i in _valid:
            x = {
                "date": i[0]["time"],
                "average": i[0]["sum_of_all_grades"] / i[0]["count_of_all_grades"],
            }
            _grades.append(x)

        df = pd.DataFrame(_grades)

        df["date"] = pd.to_datetime(df["date"], unit="s")

        print(tabulate(df, headers="keys", tablefmt="psql"))

        sns.set_style("ticks")

        plt.xticks(rotation=45)

        plt.title("Średnia ocen w czasie")
        plt.xlabel("Data")
        plt.ylabel("Średnia ocen")

        sns.lineplot(data=df, x="date", y="average")

        io_bytes = io.BytesIO()
        plt.savefig(io_bytes, format="png")
        io_bytes.seek(0)

        return base64.b64encode(io_bytes.read()).decode("ascii")
    
    # def pie_differences_summary(self, l):
    #     _valid = []

    #     todo:!

    #     print(_sizes)  

    #     fig, ax = plt.subplots()
    #     ax.pie(_sizes, labels=_labels, autopct='%1.1f%%', startangle=90)

    #     io_bytes = io.BytesIO()
    #     plt.savefig(io_bytes, format="png")
    #     io_bytes.seek(0)

    #     return base64.b64encode(io_bytes.read()).decode("ascii")


    # heat map of grades in poniedzialek - piatek model
