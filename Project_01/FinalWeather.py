"""
--------------------------------------------------------------------------
Gathering Weather Forecast (Daily Highs and Lows) from OpenWeatherMap
--------------------------------------------------------------------------
License:   
Copyright 2019 Irene Kwon

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------
Software API:
    
    * pyowm
        * Python library for OpenWeatherMap API
        * Free subscription only allows for current weather
  
--------------------------------------------------------------------------
Background Information: 
 
    * Information about pyowm
        * https://buildmedia.readthedocs.org/media/pdf/pyowm/latest/pyowm.pdf

--------------------------------------------------------------------------
Outline:
    
    - Get an API key for OpenWeather
    - Retrieve daily forecast

"""

from pyowm import OWM

#Load with the API_key for openweather
API_key  = 'ada0a3424a34c9445c81fba49df33410'
owm      = OWM(API_key)

#For Houston (city ID = 46990066)
obs      = owm.weather_at_id(4699066)

#Retrieve daily lows and highs as well as the current temperature
w        = obs.get_weather()
temp     = w.get_temperature('fahrenheit')

#Set up strings for displaying the daily forecasts
m_symbol = '\xb0' + 'F'
curr     = ('Current Temp: ', temp['temp'], m_symbol)
high     = ('Daily High: ', temp['temp_max'], m_symbol)
low      = ('Daily Low: ', temp['temp_min'], m_symbol)

#Prints the temperatures
if __name__ == '__main__':

    print(curr)
    print(high)
    print(low)