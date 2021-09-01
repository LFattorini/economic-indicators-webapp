import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.colors
from collections import OrderedDict
import requests



# default list of all countries of interest
country_default = OrderedDict([('Canada', 'CAN'), ('United States', 'USA'), 
  ('Brazil', 'BRA'), ('France', 'FRA'), ('India', 'IND'), ('Italy', 'ITA'), 
  ('Germany', 'DEU'), ('United Kingdom', 'GBR'), ('China', 'CHN'), ('Japan', 'JPN')])


def return_figures(countries=country_default):
  """Creates six plotly visualizations using the World Bank API

  Args:
      country_default (dict): list of countries for filtering the data

  Returns:
      list (dict): list containing the six plotly visualizations

  """

  # when the countries variable is empty, use the country_default dictionary
  if not bool(countries):
    countries = country_default

  # prepare filter data for World Bank API
  # the API uses ISO-3 country codes separated by ;
  country_filter = list(countries.values())
  country_filter = [x.lower() for x in country_filter]
  country_filter = ';'.join(country_filter)

  # World Bank indicators of interest for pulling data
  indicators = ['SP.POP.GROW','SL.UEM.TOTL.ZS','SL.TLF.CACT.FM.ZS', 'EN.ATM.CO2E.PC', 'NY.GDP.MKTP.KD.ZG']

  data_frames = [] # stores the data frames with the indicator data of interest
  urls = [] # url endpoints for the World Bank API

  # pull data from World Bank API and clean the resulting json
  # results stored in data_frames variable
  for indicator in indicators:
    url = 'http://api.worldbank.org/v2/countries/' + country_filter +\
    '/indicators/' + indicator + '?date=1990:2020&per_page=1000&format=json'
    urls.append(url)

    try:
      r = requests.get(url)
      data = r.json()[1]
    except:
      print('could not load data ', indicator)

    for i, value in enumerate(data):
      value['indicator'] = value['indicator']['value']
      value['country'] = value['country']['value']

    data_frames.append(data)
  
  # First chart plots population growth from 1990 to 2020 in top 10 economies 
  # as a line chart
  graph_one = []
  df_one = pd.DataFrame(data_frames[0])

  df_one.sort_values('date', ascending=True, inplace=True)

  # this  country list is re-used by all the charts to ensure legends have the same
  # order and color
  countrylist = df_one.country.unique().tolist()
  
  for country in countrylist:
      x_val = df_one[df_one['country'] == country].date.tolist()
      y_val =  df_one[df_one['country'] == country].value.tolist()
      graph_one.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name = country
          )
      )

  layout_one = dict(title = 'Population Growth Rate <br> From 1990 to 2020',
                xaxis = dict(title = 'Year',
                  autotick=False, tick0=1990, dtick=5),
                yaxis = dict(title = 'Percent'),
                )

  # second chart plots unemployment rate
    
  graph_two = []
  df_two = pd.DataFrame(data_frames[1])
    
  df_two.sort_values('date', ascending=True, inplace=True)
  
  for country in countrylist:
      x_val = df_two[df_two['country'] == country].date.tolist()
      y_val =  df_two[df_two['country'] == country].value.tolist()
      graph_two.append(
          go.Scatter(
              x = x_val,
              y = y_val,
              mode = 'lines',
              name = country
          )
      )
      
      layout_two = dict(title = 'Unemployment Rate (% of Total Labor Force) <br> From 1990 to 2020',
                        xaxis = dict(title = 'Year',
                                      autotick=False, tick0=1991, dtick=5),
                        yaxis = dict(title = 'Percent'),
                        )



  # third chart plots Ratio of female to male labor force participation rate (%) (modeled ILO estimate) from 1990 to 2020
  graph_three = []
  df_three = pd.DataFrame(data_frames[2])
  df_three.sort_values('date', ascending=True, inplace=True)

  for country in countrylist:
      x_val = df_three[df_three['country'] == country].date.tolist()
      y_val =  df_three[df_three['country'] == country].value.tolist()
      graph_three.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name = country
          )
      )

  layout_three = dict(title = 'Ratio of Female to Male Labor Force Participation Rate <br> From 1990 to 2020',
                xaxis = dict(title = 'Year',
                  autotick=False, tick0=1990, dtick=5),
                yaxis = dict(title = 'Percent'),
                )


  # fourth chart shows CO2 emissions (metric tons per capita) in 2018
  df_four = pd.DataFrame(data_frames[3])
  df_four = df_four[df_four.date == '2018']
  df_four.sort_values('value', ascending=True, inplace=True)
  
  graph_four = []


  graph_four.append(
      go.Bar(
          x = df_four.country.tolist(),
          y = df_four.value.tolist(),
      ))


  layout_four = dict(title = 'CO2 Emissions (Tons per Capita) <br> Year 2018',
                      xaxis = dict(title = 'Country'),
                      yaxis = dict(title = 'CO2 Emissions'),
                    )

# fifth graph shows GDP growth

  df_five = pd.DataFrame(data_frames[4])
  df_five.sort_values('date', ascending=True, inplace=True)

  graph_five = []

  for country in countrylist:
      x_val = df_five[df_five['country'] == country].date.tolist()
      y_val =  df_five[df_five['country'] == country].value.tolist()
      graph_five.append(
          go.Scatter(
              x = x_val,
              y = y_val,
              mode = 'lines',
              name = country
          )
      )

  layout_five = dict(title = 'GDP Growth Rate <br> From 1990 to 2020',
                      xaxis = dict(title = 'Year',
                                  autotick=False, tick0=1990, dtick=2),
                      yaxis = dict(title = 'Percent'),
                    )


  # append all charts
  figures = []
  figures.append(dict(data=graph_one, layout=layout_one))
  figures.append(dict(data=graph_two, layout=layout_two))
  figures.append(dict(data=graph_three, layout=layout_three))
  figures.append(dict(data=graph_four, layout=layout_four))
  figures.append(dict(data=graph_five, layout=layout_five))

  return figures
    