import matplotlib.pyplot as plt
import csv
import numpy as np
from decimal import Decimal
import threading
import tkinter
from tkinter import *
from tkinter import Tk
from tkinter import ttk
from tkinter import filedialog
from multiprocessing import freeze_support
import os

#Todo: Remove absolute file path for filedialog in tkinter
#Todo: Comment tkinter functions
#avg_kills_per_map and maps_played functions have division by 0 edgecases that need to be fixed ---Fixed maps_played function, need to fix avg_kills
#Pie chart needs to account for maps that aren't played to not display them ----- DONE

match_list = []

#########################################################################
#                                                                       #
#                                                                       #
#    CLASS DECLARATIONS ---> HUGE CHUNKS OF CODE                        #
#                                                                       #
#                                                                       #
#########################################################################
class Match:
	def __init__(
		self,
		map, 
		date, 
		time, 
		wait, 
		duration,
		ping, 
		kills,
		assists, 
		deaths,
		mvps,
		hsp,
		score,
		rounds_for,
		rounds_against):


		self.map = map
		self.date = date
		self.time = time
		self.wait = wait 
		self.duration = duration
		self.ping = ping
		self.kills = kills
		self.assists = assists
		self.deaths = deaths
		self.mvps = mvps
		self.hsp = hsp
		self.score = score
		self.rounds_for = rounds_for
		self.rounds_against = rounds_against

class CSV_File_Submit_GUI:
	def __init__(self, master):
		self.master = master
		master.title('Submit CSV File')
		master.geometry('700x105')
		master.resizable(False, False)

		master.rowconfigure(0, weight = 2)
		master.rowconfigure(1, weight = 1)
		master.rowconfigure(2, weight = 2)
		master.columnconfigure(0, weight = 1)
		master.columnconfigure(1, weight = 1)
		self.file_name = None
		self.csv_caption = Label(master, text = 'Select your csv file by either typing in the path or using Browse Files', bg = '#003b46', fg = '#d7e1f2', font = 'Helvetica 11 bold')
		self.csv_caption.grid(row = 0, column = 0, columnspan = 2, sticky=W+E+N+S)


		self.file = Entry(master, font = 'Helvetica 10', bd = 4)
		self.file.grid(row = 1, column = 0, columnspan = 2, ipady = 2, ipadx = 2, sticky=W+E+N+S)

		self.browse_files = Button(master, text = 'Browse Files', command = self.browse,
									  relief = 'ridge', borderwidth = 3, bg = '#c4dfe6', fg = '#07575b', font = 'Helvetica 11 bold')
		self.browse_files.grid(row = 2, column = 0, columnspan = 1, sticky=W+E+N+S)

		self.submit_file = Button(master, text = 'Submit File', command = self.read_file,
									 relief = 'ridge', borderwidth = 3, bg = '#c4dfe6', fg = '#07575b', font = 'Helvetica 11 bold')
		self.submit_file.grid(row = 2, column = 1, columnspan = 1, sticky=W+E+N+S)

	def browse(self):
		#global csv_entry_menu, file
		self.master.filename = filedialog.askopenfilename(initialdir = "C:/Users/Mike/Documents/wingman-data-scraper", title = "Select file", filetypes = (("csv files (.csv)","*.csv"),("all files","*.*")))
		self.file.delete(0,END)
		self.file.insert(0, self.master.filename)
		self.counter = 0
		try:
			with open(self.file.get(), 'r') as data_file:
				csv_data = csv.reader(data_file)
				next(csv_data)
				for row in csv_data:
					self.counter += 1

			self.master.geometry('700x180')
			self.slider_label = Label(self.master, text = 'Choose how many matches to read from, starting from your most recent match', bg = '#003b46', fg = '#d7e1f2', font = 'Helvetica 11 bold')
			self.slider_label.grid(row = 3, column = 0, columnspan = 2, sticky=W+E+N+S)
			self.match_slider = Scale(self.master, from_ = 1, to = self.counter, orient = HORIZONTAL)
			self.match_slider.grid(row = 4, column = 0, columnspan = 2, sticky=W+E+N+S)

		except (IOError, FileNotFoundError) as e:
			print("Invalid File")

	def read_file(self):
		self.file_name = self.file.get()
		count = 0
		self.counter = self.match_slider.get()
		try:
			with open(self.file_name, 'r') as data_file:
				csv_data = csv.reader(data_file)
				next(csv_data)
				for row in csv_data:
					if(count < self.counter):
						match = Match(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14])
						match_list.append(match)
						count += 1
						print(count)
					else:
						break
				self.stats_gui()

		except (IOError, FileNotFoundError) as e:
			self.file_name = None
			print(e)

	def stats_gui(self):
		self.master.title("View Your Stats")
		self.master.geometry("1000x400")
		self.csv_caption.grid_forget()
		self.file.grid_forget()
		self.browse_files.grid_forget()
		self.submit_file.grid_forget()
		self.slider_label.grid_forget()
		self.match_slider.grid_forget()

		for rows in range(0, 7):
			self.master.rowconfigure(rows, weight = 1)
		for cols in range(0, 8):
			self.master.columnconfigure(cols, weight = 1)

		self.csv_caption = Label(self.master, text = 'Last ' + str(self.counter) + ' Matches', bg = '#003b46', fg = '#d7e1f2', font = 'Helvetica 11 bold')
		self.csv_caption.grid(row = 0, column = 0, columnspan = 1, sticky=W+E+N+S)

		self.mirage_label = Label(self.master, text = 'De_Mirage', bg = '#003b46', fg = '#d7e1f2', font = 'Helvetica 11 bold')
		self.mirage_label.grid(row = 0,  column = 1, sticky=W+E+N+S)
		self.inferno_label = Label(self.master, text = 'De_Inferno', bg = '#003b46', fg = '#d7e1f2', font = 'Helvetica 11 bold')
		self.inferno_label.grid(row = 0,  column = 2, sticky=W+E+N+S)
		self.nuke_label = Label(self.master, text = 'De_Nuke', bg = '#003b46', fg = '#d7e1f2', font = 'Helvetica 11 bold')
		self.nuke_label.grid(row = 0,  column = 3, sticky=W+E+N+S)
		self.overpass_label = Label(self.master, text = 'De_Overpass', bg = '#003b46', fg = '#d7e1f2', font = 'Helvetica 11 bold')
		self.overpass_label.grid(row = 0,  column = 4, sticky=W+E+N+S)
		self.train_label = Label(self.master, text = 'De_Train', bg = '#003b46', fg = '#d7e1f2', font = 'Helvetica 11 bold')
		self.train_label.grid(row = 0,  column = 5, sticky=W+E+N+S)
		self.dust2_label = Label(self.master, text = 'De_Dust2', bg = '#003b46', fg = '#d7e1f2', font = 'Helvetica 11 bold')
		self.dust2_label.grid(row = 0,  column = 6, sticky=W+E+N+S)
		self.cache_label = Label(self.master, text = 'De_Cache', bg = '#003b46', fg = '#d7e1f2', font = 'Helvetica 11 bold')
		self.cache_label.grid(row = 0, column = 7, sticky=W+E+N+S)
		self.kills_label = Label(self.master, text = 'Average Kills', bg = '#003b46', fg = '#d7e1f2', font = 'Helvetica 11 bold')
		self.kills_label.grid(row = 1, column = 0, sticky = W+E+N+S)
		self.deaths_label = Label(self.master, text = 'Average Deaths', bg = '#003b46', fg = '#d7e1f2', font = 'Helvetica 11 bold')
		self.deaths_label.grid(row = 2, column = 0, sticky = W+E+N+S)
		self.kda_label = Label(self.master, text = 'K-D Ratio', bg = '#003b46', fg = '#d7e1f2', font = 'Helvetica 11 bold')
		self.kda_label.grid(row = 3, column = 0, sticky = W+E+N+S)
		self.map_played_num_label = Label(self.master, text = 'Map Occurence', bg = '#003b46', fg = '#d7e1f2', font = 'Helvetica 11 bold')
		self.map_played_num_label.grid(row = 4, column = 0, sticky = W+E+N+S)
		self.button_label = Label(self.master, text = 'Data Visualization Options', bg = '#1A39B1', fg = '#d7e1f2', font = 'Helvetica 11 bold')
		self.button_label.grid(row=5, column = 0, columnspan = 8, sticky=W+E+N+S)

		kda_stats = kda_table()
		button_text = ['Maps Played Chart', 'Map Win %', 'Average K-D Per Map', 'a', 'b', 'c', 'd']

		for i in range(0, len(kda_stats[0])):
			kill_label = Label(self.master, text = kda_stats[0][i], font = 'Helvetica 11', borderwidth = 1, relief = 'solid')
			kill_label.grid(row = 1, column = i + 1, sticky=W+E+N+S)
			death_label = Label(self.master, text = kda_stats[1][i], font = 'Helvetica 11', borderwidth = 1, relief = 'solid')
			death_label.grid(row = 2, column = i + 1, sticky=W+E+N+S)
			kd_label = Label(self.master, text = kda_stats[2][i], font = 'Helvetica 11', borderwidth = 1, relief = 'solid')
			kd_label.grid(row = 3, column = i + 1, sticky=W+E+N+S)
			map_played_label = Label(self.master, text = kda_stats[3][i], font = 'Helvetica 11', borderwidth = 1, relief = 'solid')
			map_played_label.grid(row = 4, column = i + 1, sticky=W+E+N+S)

		self.pie_button = Button(self.master, text = 'Pie Chart: Maps Played Distribution', command = pie_chart_maps_played,
									 relief = 'raised', borderwidth = 3, bg = '#c4dfe6', fg = '#07575b', font = 'Helvetica 11 bold')
		self.pie_button.grid(row = 6, column = 0, columnspan = 4, sticky=W+E+N+S)

		self.map_win_pct_button = Button(self.master, text = 'Bar Graph: Map Win Percentage', command = bar_graph_maps_played_vs_win_pct,
									 relief = 'raised', borderwidth = 3, bg = '#c4dfe6', fg = '#07575b', font = 'Helvetica 11 bold')
		self.map_win_pct_button.grid(row = 6, column = 4, columnspan = 4, sticky=W+E+N+S)



def pie_chart_maps_played():
	labels = {'Mirage': 0, 'Inferno': 0, 'Nuke': 0, 'Overpass': 0, 'Train': 0, 'Dust II': 0, 'Cache': 0}
	#labels = ['De_Mirage', 'De_Inferno', 'De_Nuke', 'De_Overpass', 'De_Train', 'De_Dust2', 'De_Cache']
	mirage, inferno, nuke, overpass, train, dust2, cache = 0, 0, 0, 0, 0, 0, 0
	for match in match_list:
		if(match.map.strip() == 'Mirage'):
			labels['Mirage'] += 1
		elif(match.map.strip() == 'Inferno'):
			labels['Inferno'] += 1
		elif(match.map.strip() == 'Nuke'):
			labels['Nuke'] += 1
		elif(match.map.strip() == 'Overpass'):
			labels['Overpass'] += 1
		elif(match.map.strip() == 'Train'):
			labels['Train'] += 1
		elif(match.map.strip() == 'Dust II'):
			labels['Dust II'] += 1
		elif(match.map.strip() == 'Cache'):
			labels['Cache'] += 1
		else:
			pass

	sizes = []
	sorted_label_list = []
	fig1, ax1 = plt.subplots()

	for key in list(labels.keys()):
		if(labels[key] == 0):
			pass
		else:
			sizes.append(labels[key])
			sorted_label_list.append(key)

	ax1.pie(sizes, labels = sorted_label_list, autopct='%1.1f%%')
	ax1.axis('equal')
	plt.title('Maps Played Distribution')
	plt.show()

def bar_graph_maps_played_vs_win_pct():

	#First element of the list is the counter for wins, the next is counter for total games played
	dict_labels = {'De_Mirage': [0, 0], 'De_Inferno': [0, 0], 'De_Nuke': [0, 0], 'De_Overpass': [0, 0], 'De_Train': [0, 0], 'De_Dust II': [0, 0], 'De_Cache': [0, 0]}

	width = 0.6
	for match in match_list:
		if(match.map.strip() == 'Mirage'):
			dict_labels['De_Mirage'][1] += 1
			if(int(match.rounds_for) > int(match.rounds_against)):
				dict_labels['De_Mirage'][0] += 1
		elif(match.map.strip() == 'Inferno'):
			dict_labels['De_Inferno'][1] += 1
			if(int(match.rounds_for) > int(match.rounds_against)):
				dict_labels['De_Inferno'][0] += 1
		elif(match.map.strip() == 'Nuke'):
			dict_labels['De_Nuke'][1] += 1
			if(int(match.rounds_for) > int(match.rounds_against)):
				dict_labels['De_Nuke'][0] += 1
		elif(match.map.strip() == 'Overpass'):
			dict_labels['De_Overpass'][1] += 1
			if(int(match.rounds_for) > int(match.rounds_against)):
				dict_labels['De_Overpass'][0] += 1
		elif(match.map.strip() == 'Train'):
			dict_labels['De_Train'][1] += 1
			if(int(match.rounds_for) > int(match.rounds_against)):
				dict_labels['De_Train'][0] += 1
		elif(match.map.strip() == 'Dust II'):
			dict_labels['De_Dust II'][1] += 1
			if(int(match.rounds_for) > int(match.rounds_against)):
				dict_labels['De_Dust II'][0] += 1
		elif(match.map.strip() == 'Cache'):
			dict_labels['De_Cache'][1] += 1
			if(int(match.rounds_for) > int(match.rounds_against)):
				dict_labels['De_Cache'][0] += 1
		else:
			pass

	fig, ax = plt.subplots()
	win_pcts = []
	labels = []
	for key in list(dict_labels.keys()):
		if(dict_labels[key][1] == 0):
			pass
		else:
			win_pcts.append(dict_labels[key][0]/dict_labels[key][1])
			labels.append(key)

	ind = np.arange(len(labels))
	p2 = ax.bar(ind + width / 2, win_pcts, width, color = 'b')
	ax.set_xticks(ind + width / 2)
	ax.set_xticklabels(labels)
	ax.autoscale_view()
	fig.autofmt_xdate()
	#plt.bar(labels, map_pcts, width = ind_width)
	plt.title('Map Win Percentage Comparison')
	plt.xlabel('Maps')
	plt.ylabel('Win Percentage')
	plt.show()

def avg_kills_deaths_per_map():
	labels = ['De_Mirage', 'De_Inferno', 'De_Nuke', 'De_Overpass', 'De_Train', 'De_Dust2', 'De_Cache']
	mirage, inferno, nuke, overpass, train, dust2, cache = 0, 0, 0, 0, 0, 0, 0
	mirage_kills, inferno_kills, nuke_kills, overpass_kills, train_kills, dust2_kills, cache_kills = 0, 0, 0, 0, 0, 0, 0
	mirage_deaths, inferno_deaths, nuke_deaths, overpass_deaths, train_deaths, dust2_deaths, cache_deaths = 0, 0, 0, 0, 0, 0, 0
	width = 0.35
	ind = np.arange(7)
	for match in match_list:
		if(match.map.strip() == 'Mirage'):
			mirage += 1
			mirage_kills = mirage_kills + int(match.kills)
			mirage_deaths = mirage_deaths + int(match.deaths)
		elif(match.map.strip() == 'Inferno'):
			inferno += 1
			inferno_kills = inferno_kills + int(match.kills)
			inferno_deaths = inferno_deaths + int(match.deaths)
		elif(match.map.strip() == 'Nuke'):
			nuke += 1
			nuke_kills = nuke_kills + int(match.kills)
			nuke_deaths = nuke_deaths + int(match.deaths)
		elif(match.map.strip() == 'Overpass'):
			overpass += 1
			overpass_kills =  overpass_kills + int(match.kills)
			overpass_deaths = overpass_deaths + int(match.deaths)
		elif(match.map.strip() == 'Train'):
			train += 1
			train_kills = train_kills + int(match.kills)
			train_deaths = train_deaths + int(match.deaths)
		elif(match.map.strip() == 'Dust II'):
			dust2 += 1
			dust2_kills = dust2_kills + int(match.kills)
			dust2_deaths = dust2_deaths + int(match.deaths)
		elif(match.map.strip() == 'Cache'):
			cache += 1
			cache_kills = cache_kills + int(match.kills)
			cache_deaths = cache_deaths + int(match.deaths)
		else:
			pass

	avg_kills = [mirage_kills/mirage, inferno_kills/inferno, nuke_kills/nuke, overpass_kills/overpass, train_kills/train, dust2_kills/dust2, cache_kills/cache]
	avg_deaths = [mirage_deaths/mirage, inferno_deaths/inferno, nuke_deaths/nuke, overpass_deaths/overpass, train_deaths/train, dust2_deaths/dust2, cache_deaths/cache]
	fig, ax = plt.subplots()
	p1 = ax.bar(ind, avg_kills, width, color = 'g')
	p2 = ax.bar(ind + width, avg_deaths, width, color = 'r')
	ax.set_xticks(ind + width / 2)
	ax.set_xticklabels(labels)
	ax.autoscale_view()
	fig.autofmt_xdate()
	plt.show()


#If maps played count y is 0, then return a string instead of undefined 
def safe_division(x, y):
	if(y == 0):
		return 'Map Not Played'
	else:
		return x/y

def kda_table():
	retval = []
	kda = []
	mirage, inferno, nuke, overpass, train, dust2, cache = 0, 0, 0, 0, 0, 0, 0
	mirage_kills, inferno_kills, nuke_kills, overpass_kills, train_kills, dust2_kills, cache_kills = 0, 0, 0, 0, 0, 0, 0
	mirage_deaths, inferno_deaths, nuke_deaths, overpass_deaths, train_deaths, dust2_deaths, cache_deaths = 0, 0, 0, 0, 0, 0, 0
	for match in match_list:
		if(match.map.strip() == 'Mirage'):
			mirage += 1
			mirage_kills = mirage_kills + int(match.kills)
			mirage_deaths = mirage_deaths + int(match.deaths)
		elif(match.map.strip() == 'Inferno'):
			inferno += 1
			inferno_kills = inferno_kills + int(match.kills)
			inferno_deaths = inferno_deaths + int(match.deaths)
		elif(match.map.strip() == 'Nuke'):
			nuke += 1
			nuke_kills = nuke_kills + int(match.kills)
			nuke_deaths = nuke_deaths + int(match.deaths)
		elif(match.map.strip() == 'Overpass'):
			overpass += 1
			overpass_kills =  overpass_kills + int(match.kills)
			overpass_deaths = overpass_deaths + int(match.deaths)
		elif(match.map.strip() == 'Train'):
			train += 1
			train_kills = train_kills + int(match.kills)
			train_deaths = train_deaths + int(match.deaths)
		elif(match.map.strip() == 'Dust II'):
			dust2 += 1
			dust2_kills = dust2_kills + int(match.kills)
			dust2_deaths = dust2_deaths + int(match.deaths)
		elif(match.map.strip() == 'Cache'):
			cache += 1
			cache_kills = cache_kills + int(match.kills)
			cache_deaths = cache_deaths + int(match.deaths)
		else:
			pass

	avg_kills = [safe_division(mirage_kills,mirage), safe_division(inferno_kills, inferno), safe_division(nuke_kills,nuke), safe_division(overpass_kills,overpass), 
				 safe_division(train_kills,train), safe_division(dust2_kills, dust2), safe_division(cache_kills, cache)]
	avg_deaths = [safe_division(mirage_deaths,mirage), safe_division(inferno_deaths, inferno), safe_division(nuke_deaths,nuke), safe_division(overpass_deaths,overpass), 
				  safe_division(train_deaths,train), safe_division(dust2_deaths,dust2), safe_division(cache_deaths,cache)]

	for i in range(0, len(avg_deaths)):

		if(isinstance(avg_kills[i], str)):
			kda.append('Map Not Played')
		else:
			print(avg_kills[i],avg_deaths[i])
			map_kda = Decimal(avg_kills[i]/avg_deaths[i])
			map_kda = round(map_kda, 2)
			kda.append(map_kda)
			avg_kills[i] = round(Decimal(avg_kills[i]), 2)
			avg_deaths[i] = round(Decimal(avg_deaths[i]), 2)
	retval.append(avg_kills)
	retval.append(avg_deaths)
	retval.append(kda)
	retval.append([mirage, inferno, nuke, overpass, train, dust2, cache])
	return retval


if __name__ == '__main__':
	freeze_support()
	global file_name
	root = Tk()
	test_gui = CSV_File_Submit_GUI(root)
	root.mainloop()


