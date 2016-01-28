#!/usr/bin/env python

from __future__ import print_statement

import os
import subprocess

import pymzml

msconvert_path = r"C:\Users\Nader\Dropbox (MIT)\White Lab\CAMV\ProteoWizard\ProteoWizard 3.0.9205\msconvert.exe"
raw_dir = r"C:\Users\Nader\Dropbox (MIT)\White Lab\Axonal Degeneration\MS RAW"
files = [
	"2015-10-09-NH7-1-6-1-pY-imac27-elute-pre37-colAaron3.mzML",
	"2015-10-21-NH7-7-12-1-pY-imac14-elute-pre39-colAaron3.mzML"
]

whitelist = [744.34, 744.84]
blacklist = [743.84, 744.60]
mass_range = (743, 746)
min_i = 1e4

for file in files:
	path = os.path.join(raw_dir, file)
	
	if os.path.splitext(path)[1].lower() in [".raw"]:
		mzml_path = os.path.splitext(path)[0] + ".mzML"
		
		if not os.path.exists(mzml_path):
			cmd = [
				msconvert_path,
				path,
				"--mzML",
			]
			subprocess.check_call(cmd)
		
		path = mzml_path
		
	print("{}:".format(file))
	m = pymzml.run.Reader(path)
	
	for scan in m:
		if scan["ms level"] is None or int(scan["ms level"]) != 1:
			continue
			
		if any(scan.hasPeak(i) for i in blacklist):
			continue
		
		if all(scan.hasPeak(i) for i in whitelist):
			print("\t#{}: {}".format(scan["id"], mass_range))
			
			# Print all neighboring peaks > minimum intensity
			for mz, i in scan.peaks:
				if mz > mass_range[0] and mz < mass_range[1] and i > min_i:
					print("\t\t{}: {}".format(mz, i))
