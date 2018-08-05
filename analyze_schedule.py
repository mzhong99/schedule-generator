import json
import pprint
from collections import deque

# once instantiated, can only generate schedule once before it's used
# TODO: cache all current classes. too much valuable info and i'm getting tired of typing this all in again

class StudyPlanGenerator:

	semester_number = 0
	course_data = []
	initially_taken_courses = []

	taken_courses = set()
	remaining_courses = set()

	schedule = []

	def __init__(self, course_data, initially_taken_courses, credit_threshold=16):
		self.course_data = course_data
		self.initially_taken_courses = initially_taken_courses
		
		self.taken_courses = set(initially_taken_courses)
		self.remaining_courses = set(self.course_data.keys()).difference(self.taken_courses)

		for course_info in self.course_data.values():
			course_info["unlocks"] = set()

		self.generate_unlocks()
		self.generate_unlock_potential()

	def generate_unlocks(self):
		for course in self.course_data.keys():
			for potential_neighbor in self.course_data.keys():
				if course in course_data[potential_neighbor]["prerequisites"]:
					course_data[course]["unlocks"].add(potential_neighbor)
		pass

	def generate_unlock_potential(self):
		for course_name in course_data.keys():
			self.generate_single_unlock_potential(course_name)

	def generate_single_unlock_potential(self, start_course_name):
		
		queue = deque()
		seen = set()
		queue.append(start_course_name)
		
		while len(queue) is not 0:
			current = queue.popleft()
			for unlock in self.course_data[current]["unlocks"]:
				if current not in seen:
					seen.add(current)
					queue.append(current)

		# seen.remove(start_course_name)
		self.course_data[start_course_name]["unlock_potential"] = len(seen)
		self.course_data[start_course_name]["children"] = seen

		pass

	def print_course_graph(self):
		pprint.pprint(course_data)
		pass

	# this function is apparently an example of the knapsack problem.
	# there's a better way to do this probably but for now i'll use just a greedy unlock potential pick
	# the real solution of this problem is NP complete, possibly use dynamic programming to solve
	# returns a tuple of semester set and credit count that semester
	def get_next_semester(self, credit_threshold):
		
		semester = set()
		credit_count = 0
		
		available = [course_name for course_name in self.remaining_courses 
								 if self.course_is_available(course_name)]
		available = sorted(available, key=lambda course_name : self.course_data[course_name]["unlock_potential"], reverse=True)
		
		for course_name in available:
			if credit_count + self.course_data[course_name]["credits"] < credit_threshold:
				credit_count += self.course_data[course_name]["credits"]
				semester.add(course_name)

		self.remaining_courses = self.remaining_courses.difference(semester)
		self.taken_courses = self.taken_courses.union(semester)

		return semester, credit_count

	def course_is_available(self, course_name):
		is_available = True
		for prerequisite in self.course_data[course_name]["prerequisites"]:
			if prerequisite not in self.taken_courses:
				is_available = False
		return is_available

	def generate_schedule(self, credit_threshold):
		if int(credit_threshold) > 19 or int(credit_threshold) < 12:
			print("Credit threshold outside of range [12-19]. Enter a valid credit threshold for schedule analysis.")
			return None

		while len(self.remaining_courses) > 0:
			
			start_courses_count = len(self.remaining_courses)

			self.schedule.append(self.get_next_semester(int(credit_threshold)))
			self.semester_number += 1
			print("Generated schedule for semester " + str(self.semester_number))

			if start_courses_count == len(self.remaining_courses):
				print("[WARNING] Unreachable courses:")
				for course in self.remaining_courses:
					print("[UNREACHABLE] " 
						 + course + " " 
						 + self.course_data[course]["human_name"])
				break
		print("Finished generating all semesters.")

		pass

	def retrieve_schedule(self):
		return self.schedule

	def fancy_print(self):
		semester_number = 1
		for semester_plan in self.schedule:
			print("===============================================")
			print("Semester " + str(semester_number) + ": " 
				+ str(semester_plan[1]) + " credits")
			print("-----------------------------------------------")
			for course in semester_plan[0]:
				print(course + " " + self.course_data[course]["human_name"])
			semester_number += 1
		pass


if __name__ == "__main__":
	
	major = input("Enter major data to analyze schedule: ")
	
	json_name = major + "_revised.json"
	csv_name = major + ".csv"

	course_data = []
	initially_taken_courses = []

	with open(json_name) as file:
		course_data = json.load(file)

	with open(csv_name) as file:
		initially_taken_courses = file.readlines()[1].split(",")

	spg = StudyPlanGenerator(course_data, initially_taken_courses)
	# spg.print_course_graph()
	credit_max = input("Enter how many maximum credits you want in one semester: ")
	spg.generate_schedule(credit_max)
	spg.fancy_print()
	