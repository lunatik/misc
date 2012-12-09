#author: Angel Ivanvv
#  date: 9 Dec 2012

import os
import subprocess
#TODO: refactor:
#class file:
#class file_seq:
#inherit file class for exr file and override some methods (such as the way we check if the file is valid/usable)

class image_sequence:
	def __init__(self, directory, ext):
		self.directory = directory
		self.ext = ext
		#check if directory exists
		self.dir_exists = os.access(directory, os.F_OK)
		if self.dir_exists:
			self.frames = os.listdir(directory)
			self.num_of_frames = len(self.frames)
			self.empty = True
			if self.num_of_frames > 0:
				self.frame_num_sep = self.get_frame_num_separator()
				self.frame_name = self.frames[0].rsplit('.', 1)[0].rsplit(self.frame_num_sep, 1)[0]
				self.frame_padded = self.frames[0].rsplit('.', 1)[0].rsplit(self.frame_num_sep, 1)[1] 
				self.padding = len(self.frame_padded)
				self.frame_range = self.get_frame_range()
				self.missing_frames = self.get_missing_frames()
				self.existing_frames = self.get_existing_frames()
				self.seq_length = (self.frame_range[1] - self.frame_range[0]) + 1
				self.broken_frames = self.get_broken_frames()
				self.empty = False
		#put somewhere check/warning if no images (initialize with extension?!

	def get_frame_num_separator(self):
		separator = None
		frame = self.frames[0]
		frame_spl = frame.rsplit('.', 1)
		frame_sep = frame_spl[0].rsplit('_', 1)
		if len(frame_sep) == 2:
			separator = '_'
		else:
			separator = '.'
		return separator

	#PADDING
	def get_padding(self):
		return self.padding

	def add_padding(self, num, padding): #use zfill
		while len(num) < padding:
			num = '0' + num
		return num

	def remove_padding(self, frame_padded):
		frame = frame_padded.rsplit('.', 1)[0].rsplit(self.frame_num_sep, 1)[1]
		if frame[self.padding - 1] == '0':
			frame = '0'
		else:
			while frame[0] == '0':
				frame = frame[1:]
		return int(frame)

	#PADDING_END

	def get_frame_range(self):
		file_start = self.frames[0]
		file_end = self.frames[len(self.frames) - 1]
		fr_start = self.remove_padding(file_start)
		fr_end = self.remove_padding(file_end)
		frame_range = [fr_start, fr_end]
		return frame_range

	def get_existing_frames(self):
		existing_frames = []
		for frame in self.frames:
			if frame in self.missing_frames:
				pass
			else:
				existing_frames.append(frame)
		return existing_frames

	def get_missing_frames(self):
		missing = []
		cntr = int(self.frame_range[0])
		while cntr < int(self.frame_range[1]):
			frame = '%s%s%s.%s' % (self.frame_name, self.frame_num_sep, self.add_padding(str(cntr), self.padding), self.ext)
			if frame not in self.frames:
				missing.append(frame)
			cntr += 1
		return missing

	def is_valid(self, frame):
		valid = False
		if os.name == 'nt':
			cmd = '/path/to/tool/validating/image.files'
			file_path = '%s\%s' % (self.directory, frame)
			eval_cmd = '%s \"%s\"' % (cmd, file_path)
			status = subprocess.Popen(eval_cmd, stderr=subprocess.PIPE).communicate()[1]
			if len(status) > 0:
				valid = False
			else:
				valid = True
		return valid

	def get_broken_frames(self):
		broken_frames = []
		for frame in self.existing_frames:
			frame_status = self.is_valid(frame)
			if frame_status == False:
				broken_frames.append(frame)
		return broken_frames
