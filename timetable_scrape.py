from vt_timetable import Timetable
from pprint import pprint
import csv
import json
import datetime

timetable = Timetable()

# pprint(timetable.unrefined_crn_lookup(crn_code = '82920', term_year = '201809'))

# test_crn = timetable.refined_lookup(subject_code = 'ECE', class_number = '2574', term_year = '201809')[0][0]
# pprint(timetable.unrefined_crn_lookup(crn_code = test_crn, term_year = '201809'))

def name2stats(name):
	values = name.split(" ")
	subject_code = values[0]
	class_number = values[1]
	term_year = str(datetime.datetime.now().year) + "09"

	course_report = timetable.refined_lookup(subject_code = subject_code, 
											 class_number = class_number, 
											 term_year = "201809")
	if not course_report:
		course_report = timetable.refined_lookup(subject_code = subject_code, 
											     class_number = class_number, 
											     term_year = str(datetime.datetime.now().year) + "01")
		term_year = str(datetime.datetime.now().year) + "01"

	if not course_report:
		return None

	crn_code = course_report[0][0]
	data = timetable.unrefined_crn_lookup(crn_code, term_year)
	
	return data

if __name__ == "__main__":
	
	print("CSV Protocol")
	print("Line 1: All classes needed to graduate")
	print("Line 2: All classes currently taken")
	
	filename = input("Enter filename of the CSV to be analyzed: ")

	csv_name = filename + ".csv"
	json_name = filename + ".json"
	csv_content = []
	total_courses = []

	with open(csv_name) as file:
		csv_content = file.readlines()

	total_courses = [course.strip() for course in csv_content[0].split(',')]

	course_stats = []

	success_courses = set()
	fail_fetch_courses = set()
	fail_exception_courses = set()

	for course in total_courses:
		
		try:
			fetched = name2stats(course)
			if fetched:
				print("[SUCCESS] Analyzed " + course)
				success_courses.add(course)
			else:
				print("[FAILED][NO FETCH] Analyzed " + course)
				fail_fetch_courses.add(course)
			course_stats.append(fetched)
			
		except Exception as ex:
			course_stats.append(None)
			print("[FAILED][EXCEPTION] Analyzed " + course)
			fail_exception_courses.add(course)



	print("Success Rate: " + str(100.0 * len(success_courses) / len(total_courses)) + "%")
	print("No-Fetch Rate: " + str(100.0 * len(fail_fetch_courses) / len(total_courses)) + "%")
	print("Exception Rate: " + str(100.0 * len(fail_exception_courses) / len(total_courses)) + "%")

	course_dict = dict(zip(total_courses, course_stats))
	for course_info in course_dict.values():
		
		if not course_info:
			continue
		
		extraneous = []
		
		for prereq in course_info["prerequisites"]:
			if prereq not in total_courses:
				extraneous.append(prereq)
		for prereq in extraneous:
			course_info["prerequisites"].remove(prereq)
	
	print("[RETRIEVAL] Attempting to retrieve [FAILED] courses from cache...")

	cache = dict()
	cache_retrieval_count = 0
	try:
		needs_retrieval = [course for course in course_dict.keys() 
		                          if course_dict[course] == None]
		with open("cache.json", "r") as cache_file:
			cache = json.load(cache_file)
		for course in needs_retrieval:
			if course in cache.keys():
				course_dict[course] = cache[course]
				cache_retrieval_count += 1
				print("[SUCCESS][RETRIEVAL] Retrieved " + course + " from cache")
			else:
				print("[FAILED][RETRIEVAL][NO CACHE] Failed to retrieve " + course + " from cache")

	except Exception:
		print("[FAILED][RETRIEVAL][EXCEPTION] Error retrieving from cache.")
		
	print("Cache Retrieval Rate: " + str(100.0 * cache_retrieval_count / len(total_courses)) + "%")

	print("Analysis complete. Dumping...")

	with open(json_name, 'w+') as target:
		json.dump(course_dict, target)

	print("Dumping complete. File: " + json_name)

