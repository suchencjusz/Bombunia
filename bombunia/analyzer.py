import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import numpy
import io
import base64

from PIL import Image

from tabulate import tabulate


class Analyzer:
    def fig2data ( fig ):
        """
        @brief Convert a Matplotlib figure to a 4D numpy array with RGBA channels and return it
        @param fig a matplotlib figure
        @return a numpy 3D array of RGBA values
        """
        # draw the renderer
        fig.canvas.draw ( )
    
        # Get the RGBA buffer from the figure
        w,h = fig.canvas.get_width_height()
        buf = numpy.fromstring ( fig.canvas.tostring_argb(), dtype=numpy.uint8 )
        buf.shape = ( w, h,4 )
    
        # canvas.tostring_argb give pixmap in ARGB mode. Roll the ALPHA channel to have it in RGBA mode
        buf = numpy.roll ( buf, 3, axis = 2 )
        return buf

    def fig2img ( fig ):
        """
        @brief Convert a Matplotlib figure to a PIL Image in RGBA format and return it
        @param fig a matplotlib figure
        @return a Python Imaging Library ( PIL ) image
        """
        # put the figure pixmap into a numpy array
        buf = Analyzer.fig2data ( fig )
        w, h, d = buf.shape
        return Image.fromstring( "RGBA", ( w ,h ), buf.tostring( ) )

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

        return 0


    def pie_differences_summary(self, l):
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
        
        return Analyzer.fig2img(fig)

        # return PIL.Image.frombytes('RGB',fig.canvas.get_width_height(),fig.canvas.tostring_rgb())

        


    # heat map of grades in poniedzialek - piatek model
