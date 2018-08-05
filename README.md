# schedule-generator
Webscraping, Caching, and Analytical tools to generate study plans for majors in Virginia Tech!

This set of script files can be used to generate a study plan for any major at Virginia Tech. The timetable_scrape.py file takes in a csv which contains the classes required for one student's major, and attempts to fetch the number of credits and prerequisites for each course and save this data into a json file. Since the webscraper is not always successful, manual revisions can be made to the json before the json is fed to the analyze_schedule.py, which generates a schedule based on the data inside the json. Additionally, the cache.py file allows the user to save the data for all their probed and manually-entered courses so that upon repeated use, the timetable_scrape.py script can also retrieve data from cache if it is unable to scrape https://banweb.banner.vt.edu/ssb/prod/HZSKVTSC.P_ProcRequest for the course data.

The vt_timetable.py module is directly modified from https://github.com/kevincianfarini/pyvt/, which was given with the proper license:

The MIT License (MIT)

Copyright (c) 2016 Kevin Cianfarini

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
