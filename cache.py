import json
import time

if __name__ == "__main__":
	
	addition_file_name = input("Enter filename of additional classes to be added: ")

	start_time = time.time()

	cache = dict()

	# =======================================================
	with open("cache.json", "r") as file_in:
		cache = json.load(file_in)
	# =======================================================
	
	try:
		addition = dict()
		with open(addition_file_name, "r") as additional_file:
			addition = json.load(additional_file)
		
		for key in addition.keys():
			if key not in cache.keys():
				cache[key] = addition[key]

	except Exception:
		print("File not found or invalid.")

	# =======================================================
	with open("cache.json", "w") as file_out:
		json.dump(cache, file_out, indent=4, sort_keys=True)
	# =======================================================

	end_time = time.time()
	elapsed_time = end_time - start_time

	print("Finished (" + str(elapsed_time)[:5] + " sec)")