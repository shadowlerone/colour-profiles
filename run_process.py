#!/usr/bin/env python
from multiprocessing import process
import sys
import processes

if __name__ == "__main__":
	full = False
	if "--full" in sys.argv:
		# process.full_test()
		full = True
	elif "--t" in sys.argv:
		test = True
	if not full:
		if "-f" in sys.argv:
			fi = sys.argv.index("-f")
			if len(sys.argv) >= fi + 2:
				# print(sys.argv[fi + 1])
				fp = sys.argv[fi + 1]
			else:
				print("No file specified...")
				sys.exit(0)
	if "-p" in sys.argv:
		print("process specified")
		pi = sys.argv.index("-p")
		if len(sys.argv) >= pi + 2:
			pp = sys.argv[pi + 1]
			if pp not in processes.processes.keys():
				print("Process doesn't exist")
				sys.exit()
			else:
				print(pp)
				if full:
					print("full test")
					processes.processes[pp].full_test()
				elif test:
					print("part test")
					processes.processes[pp].test()
				else:
					processes.processes[pp](fp)
		else:
			print("no process specified")
			sys.exit(0)
	else:
		# print(len(processes.processes))
		for p in processes.processes.values():
			print(f"saving {p.name}")
			if test:
				p.test()
			else:
				p.full_test()