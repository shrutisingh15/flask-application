from flask import Flask, render_template,request
import pandas as pd
from datetime import date
from bokeh.plotting import figure
from bokeh.charts import Bar, output_file, show, output_notebook,Line
from bokeh.embed import file_html, components
from bokeh.models import HoverTool, BoxSelectTool, BoxAnnotation
from bokeh.plotting import figure, ColumnDataSource



app = Flask(__name__)
@app.route('/',methods=['GET','POST'])
def indexDataPage():
    return render_template('indexdata.html')
      

@app.route('/index',methods=['GET','POST'])
def stockDataPage():
    
    stock = request.form['ticker']
    
    selected = request.form.getlist('features')
    
    datasource=pd.read_csv('https://www.quandl.com/api/v3/datasets/WIKI/%s.csv?api_key=yzehuYgEE7pyJXgrwWN9' %(stock), parse_dates=["Date"])

    hover = HoverTool(
        tooltips =[("Price","$y")]       
    )
    
    
    
    plot = figure(tools = [hover],title = 'Data from Quandl WIKI set',x_axis_label='date',y_axis_label='Price',x_axis_type='datetime',title_text_font_size='18pt')
    plot.outline_line_width = 5
    plot.outline_line_alpha = 0.3
    plot.outline_line_color = "navy"
    plot.xaxis.axis_label = "Date"
    plot.yaxis.axis_label = "Price"
    data = ColumnDataSource(datasource)
    for features in selected :
        if features == 'Close':
           line_color = 'red'
        if features == 'Adj. Close':
           line_color = 'blue'
        if features == 'Open':
           line_color = 'green'
        if features == 'Adj. Open':
           line_color = 'gray' 
        legendname = stock + ": "+features
        plot.line('Date',features,line_color=line_color,line_width=1,legend=legendname,source=data)
    script,div = components(plot)
    return render_template('stockdata.html',script=script,div=div,ticker=stock)
    
                  
if __name__ == '__main__':
    app.debug = True
    app.run(port=33507)

  

