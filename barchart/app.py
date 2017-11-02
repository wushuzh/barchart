from flask import Flask, render_template
import random
from bokeh.embed import components
from bokeh.models.sources import ColumnDataSource
from bokeh.models import (FactorRange, Range1d, LinearAxis, Grid,
                          HoverTool)
from bokeh.plotting import figure
from bokeh.models.glyphs import VBar
from bokeh.resources import INLINE


app = Flask(__name__)


@app.route("/<int:bars_count>/")
def cahrt(bars_count):
    if bars_count <= 0:
        bars_count = 1

    data = {"days": [], "bugs": [], "costs": []}
    for i in range(1, bars_count + 1):
        data['days'].append(str(i))
        data['bugs'].append(random.randint(1, 100))
        data['costs'].append(random.uniform(1.00, 1000.00))

    hover = create_hover_tool()
    plot = create_bar_chart(data, "Bugs found per days", "days", "bugs",
                            hover)
    script, div = components(plot)

    return render_template("chart.html", bars_count=bars_count,
                           the_div=div, the_script=script,
                           js_resources=INLINE.render_js(),
                           css_resources=INLINE.render_css())


def create_bar_chart(data, title, x_name, y_name, hover_tool=None,
                     width=1200, height=300):
    """Creates a barchart plot with the exact styling for the centcom
       dashboard, Pass in data as a dictionary, desired plot title,
       name of x axis, y axis.
    """
    source = ColumnDataSource(data)
    xdr = FactorRange(factors=data[x_name])
    ydr = Range1d(start=0, end=max(data[y_name]) * 1.5)

    tools = []
    if hover_tool:
        tools = [hover_tool, ]

    plot = figure(title=title, x_range=xdr, y_range=ydr, tools=tools,
                  plot_width=width, plot_height=height,
                  toolbar_location="above")

    glyph = VBar(x=x_name, width=.8, top=y_name, fill_color="#e12127")
    plot.add_glyph(source, glyph)

    xaxis = LinearAxis()
    yaxis = LinearAxis()

    plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
    plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))
    plot.yaxis.axis_label = "Bugs found"
    plot.xaxis.axis_label = "Days after app deployment"

    plot.toolbar.logo = None
    plot.xgrid.grid_line_color = None
    plot.xaxis.major_label_orientation = 1

    return plot


def create_hover_tool():
    """Generates the HTML for the Bokeh's hover data tool on our graph"""
    hover_html = """
      <div>
        <span class="hover-tooltip">$x</span>
      </div>
      <div>
        <span class="hover-tooltip">@bugs bugs</span>
      </div>
      <div>
        <span class="hover-tooltip">$@costs{0.00}</span>
      </div>
    """
    return HoverTool(tooltips=hover_html)


if __name__ == "__main__":
    app.run(debug=True)

