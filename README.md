# schedule-generator
Webscraping, Caching, and Analytical tools to generate study plans for majors in Virginia Tech!

This set of script files can be used to generate a study plan for any major at Virginia Tech. The timetable_scrape.py file takes in a csv which contains the classes required for one student's major, and attempts to fetch the number of credits and prerequisites for each course and save this data into a json file. Since the webscraper is not always successful, manual revisions can be made to the json before the json is fed to the analyze_schedule.py, which generates a schedule based on the data inside the json. Additionally, the cache.py file allows the user to save the data for all their probed and manually-entered courses so that upon repeated use, the timetable_scrape.py script can also retrieve data from cache if it is unable to scrape https://banweb.banner.vt.edu/ssb/prod/HZSKVTSC.P_ProcRequest for the course data.

Let's go over each of the individual components and see how they work.

## the timetable_scrape.py

Run `timetable_scrape.py` first. Upon running it, the program prompts you with the filename which contains the following information:

Line 1: Comma separated values of each course code (ex: `MATH 1225`) in the major desired.
Line 2: comma separated values of each course you have already taken.

As an example, let's use my own CSV file for Computer Engineering: `cpe.csv`

```
CHEM 1035,CHEM 1045,PHYS 2305,PHYS 2306,MATH 1225,MATH 1226,MATH 2204,MATH 2534,MATH 2114,MATH 2214,ENGE 1215,ENGE 1216,ESM 2104,MUS 1005,PHIL 1304,HIST 1215,HIST 1216,PSCI 1014,ALS 1004,STAT 4714,ENGL 3764,ISE 2014,ECE 2014,ECE 2704,ECE 2504,ECE 2004,ECE 2074,ECE 2204,ECE 2274,ECE 2704,ECE 1574,ECE 2574,ECE 3574,ECE 2534,ECE 2524,ECE 3544,ECE 4534,ECE 4525,ECE 4526,ECE 4424,ECE 4524,ECE 4554,ECE 4580
CHEM 1035,CHEM 1045,PHYS 2305,PHYS 2306,MATH 1225,MATH 1226,MATH 2204,MATH 2534,MATH 2114,MATH 2214,ENGE 1215,ENGE 1216,ESM 2104,MUS 1005,PHIL 1304,HIST 1215,HIST 1216,PSCI 1014,ECE 1574
```

Note: the file extension is already handled for you. In my case, the command prompt looks like this:

```
CSV Protocol
Line 1: All classes needed to graduate
Line 2: All classes currently taken
Enter filename of the CSV to be analyzed: cpe
                                          ^^^
```

The `timetable_scrape.py` then analyzes each class for their credits and prerequisites. In my case, this is what the logs look like:

```
[SUCCESS] Analyzed CHEM 1035
[SUCCESS] Analyzed CHEM 1045
[FAILED][EXCEPTION] Analyzed PHYS 2305
[SUCCESS] Analyzed PHYS 2306
[FAILED][EXCEPTION] Analyzed MATH 1225
[SUCCESS] Analyzed MATH 1226
[SUCCESS] Analyzed MATH 2204
[SUCCESS] Analyzed MATH 2534
[SUCCESS] Analyzed MATH 2114
[SUCCESS] Analyzed MATH 2214
[SUCCESS] Analyzed ENGE 1215
[SUCCESS] Analyzed ENGE 1216
[SUCCESS] Analyzed ESM 2104
[FAILED][NO FETCH] Analyzed MUS 1005
[FAILED][EXCEPTION] Analyzed PHIL 1304
[FAILED][NO FETCH] Analyzed HIST 1215
[FAILED][NO FETCH] Analyzed HIST 1216
[SUCCESS] Analyzed PSCI 1014
[SUCCESS] Analyzed ALS 1004
[FAILED][NO FETCH] Analyzed STAT 4714
[SUCCESS] Analyzed ENGL 3764
[SUCCESS] Analyzed ISE 2014
[SUCCESS] Analyzed ECE 2014
[SUCCESS] Analyzed ECE 2704
[SUCCESS] Analyzed ECE 2504
[SUCCESS] Analyzed ECE 2004
[SUCCESS] Analyzed ECE 2074
[SUCCESS] Analyzed ECE 2204
[SUCCESS] Analyzed ECE 2274
[SUCCESS] Analyzed ECE 2704
[SUCCESS] Analyzed ECE 1574
[SUCCESS] Analyzed ECE 2574
[SUCCESS] Analyzed ECE 3574
[FAILED][EXCEPTION] Analyzed ECE 2534
[SUCCESS] Analyzed ECE 2524
[SUCCESS] Analyzed ECE 3544
[FAILED][NO FETCH] Analyzed ECE 4534
[FAILED][NO FETCH] Analyzed ECE 4525
[FAILED][NO FETCH] Analyzed ECE 4526
[SUCCESS] Analyzed ECE 4424
[FAILED][NO FETCH] Analyzed ECE 4524
[SUCCESS] Analyzed ECE 4554
[FAILED][NO FETCH] Analyzed ECE 4580
Success Rate: 67.44186046511628%
No-Fetch Rate: 20.930232558139537%
Exception Rate: 9.30232558139535%
[RETRIEVAL] Attempting to retrieve [FAILED] courses from cache...
[SUCCESS][RETRIEVAL] Retrieved PHYS 2305 from cache
[SUCCESS][RETRIEVAL] Retrieved MATH 1225 from cache
[SUCCESS][RETRIEVAL] Retrieved MUS 1005 from cache
[SUCCESS][RETRIEVAL] Retrieved PHIL 1304 from cache
[SUCCESS][RETRIEVAL] Retrieved HIST 1215 from cache
[SUCCESS][RETRIEVAL] Retrieved HIST 1216 from cache
[SUCCESS][RETRIEVAL] Retrieved STAT 4714 from cache
[FAILED][RETRIEVAL][NO CACHE] Failed to retrieve ECE 2534 from cache
[SUCCESS][RETRIEVAL] Retrieved ECE 4534 from cache
[SUCCESS][RETRIEVAL] Retrieved ECE 4525 from cache
[FAILED][RETRIEVAL][NO CACHE] Failed to retrieve ECE 4526 from cache
[FAILED][RETRIEVAL][NO CACHE] Failed to retrieve ECE 4524 from cache
[FAILED][RETRIEVAL][NO CACHE] Failed to retrieve ECE 4580 from cache
Cache Retrieval Rate: 20.930232558139537%
Analysis complete. Dumping...
Dumping complete. File: cpe.json
```

Keep in mind that `[FAILED][NO FETCH]` means that the course was not on the VT Timetable, and that `[FAILED][EXCEPTION]` means that vt_timetable.py threw an exception when attempting to find this course.

Once analysis is finished, if not all classes are fetched correctly, you may need to manually edit the `cpe.json` file yourself. You must save it in the format `youroriginalfilename_revised.json`. 

For reference, the proper form for each entry in the json file should look like this:

```
{
    "AAEC 1005": {
        "credits": 3,
        "human_name": "Econ Food Fiber Sys",
        "prerequisites": []
    },
    "AOE 3054": {
        "credits": 3,
        "human_name": "AOE Experimental Methods",
        "prerequisites": [
            "AOE 3014",
            "AOE 3024",
            "AOE 3034"
        ]
    },
    ...
}
```

Please note: the cache file I use is currently unavailable to avoid copyright problems with Virginia Tech. It is expected that you build your own cache as you continue to use this program. You must supply your own `cache.json` with classes you enter. Ensure your cache has at least one course in it before running...

## the cache.py

The cache.py script is there so that you don't have to keep manually typing in overlapping classes on repeat use. A sample cache might look like this `cache.json`:

```
{
    "DEBUG": {
        "credits": 0,
        "human_name": "DEBUG COURSE",
        "prerequisites": []
    },
    "ECE 1574": {
        "credits": 3,
        "human_name": "Engr Problem Solving with C++",
        "prerequisites": [
            "ENGE 1215",
            "MATH 1225"
        ]
    }
}
```

To add classes to your cache.json, run the program like this:

```
C:\super\duper\fake\directory>python cache.py
Enter filename of additional classes to be added: cpe_cyber_cs_revised.json
Finished (0.021 sec)
                                                                       ^^^^
```

Note that for this caching program, the file extension IS NEEDED.

## the analyze_schedule.py

So you've created your updated `filename_revised.json` and want to find an optimal schedule. In my case, I have a `cpe_revised.json`, so I simply need to run the program like this:

```
C:\super\duper\fake\directory>python analyze_schedule.py
Enter major data to analyze schedule: cpe
Enter how many maximum credits you want in one semester: 18
Generated schedule for semester 1
Generated schedule for semester 2
Generated schedule for semester 3
Generated schedule for semester 4
Finished generating all semesters.
===============================================
Semester 1: 16 credits
-----------------------------------------------
ECE 2504 Intro Computer Engr
ALS 1004 Ag, Arts and Society
ECE 2574 Data Structures and Algorithms
STAT 4714 Probability and Statistics for ECE
ECE 2014 Engr Professionalism ECE
ECE 2004 Electric Circuit Analysis
ECE 2074 Electric Circuit Analysis Lab
===============================================
Semester 2: 16 credits
-----------------------------------------------
ISE 2014 Engineering Economy
ECE 3574 Applied Software Design
ECE 4424 Machine Learning
ECE 2274 Elctrnc Netwks Lab I
ECE 2704 Signals and Systems
ECE 2534 Microcontroller Interfacing
===============================================
Semester 3: 17 credits
-----------------------------------------------
ECE 2204 Electronics
ECE 2524 Intro to Unix for Engineers
ECE 4554 Intro to Computer Vision
ECE 4524 Artificial Intelligence and Engineering Applications
ECE 4534 Embedded System Design
ECE 4525 Video Game Design and Programming
===============================================
Semester 4: 13 credits
-----------------------------------------------
ECE 4580 Digital Image Processing
ENGL 3764 Technical Writing
ECE 3544 Digital Design I
ECE 4526 Video Game Design and Programming II

```

That's it! Now go compare it with your actual schedule and see just how much it differs. Note: Corequisites, Major Restrictions, and Duplicate courses do not register well with this program. Use with care!

## copyright and extras

Special thanks to Kevin Cianfarini, for his generously offered open-source API in python. Without his work, I would never have understood how to webscrape for classes on the timetable.

The vt_timetable.py module is directly modified from https://github.com/kevincianfarini/pyvt/, which was given with the proper license:

The MIT License (MIT)

Copyright (c) 2016 Kevin Cianfarini

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
