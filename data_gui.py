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
#Modifiy bar graph to be stacked bar graph to show win/tie/loss pct on each map

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

	def back_to_main_menu(self, master):
		self.remove_widgets()
		self.master = master
		master.title('Submit CSV File')
		master.geometry('700x105')
		master.resizable(False, False)

		master.rowconfigure(0, weight = 2)
		master.rowconfigure(1, weight = 1)
		master.rowconfigure(2, weight = 2)
		master.columnconfigure(0, weight = 1)
		master.columnconfigure(1, weight = 1)

		#Needed to reconfigure the rows and columns to 0 weight
		for rows in range(3, 20):
			master.rowconfigure(rows, weight = 0)
		for column in range(2, 20):
			master.columnconfigure(column, weight = 0)

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
					else:
						break
				self.stats_gui()

		except (IOError, FileNotFoundError) as e:
			self.file_name = None
			print(e)

	def stats_gui(self):
		self.master.title("View Your Stats")
		self.master.geometry("1280x450")

		self.remove_widgets()
		

		for rows in range(0, 11):
			self.master.rowconfigure(rows, weight = 1)
		for cols in range(0, 8):
			self.master.columnconfigure(cols, weight = 1)

		#Procedurally generates the captions at the top row of the table
		horizontal_labels = ['Last ' + str(self.counter) + ' Matches', ' De_Mirage ', 'De_Inferno', '  De_Nuke  ', 'De_Overpass', ' De_Train ', 'De_Dust II', ' De_Cache ']
		counter = 0
		for label in horizontal_labels:
			caption = Label(self.master, text = label, bg = '#003b46', fg = '#d7e1f2', font = 'Helvetica 11 bold')
			caption.grid(row = 0, column = counter, columnspan = 1, sticky=W+E+N+S)
			counter += 1

		#Procedurally generates the captions at the first column of the table, skipping the first one because it was generated in the previous lines
		vertical_labels = ['Average Kills', 'Average Deaths', 'K-D Ratio', 'Map Played Frequency', 'Map Winrate %', 'Average Headshot %', 'Average MVPs/Game']
		counter = 1
		for label in vertical_labels:
			caption = Label(self.master, text = label, bg = '#003b46', fg = '#d7e1f2', font = 'Helvetica 11 bold')
			caption.grid(row = counter, column = 0, columnspan = 1, sticky=W+E+N+S)
			counter +=1

		all_match_stats = kda_table()
		all_match_stats_keys = list(all_match_stats.keys())

		i = 0
		for key in all_match_stats_keys:
			if(all_match_stats[key]['Matches Played'] == '-'):
				kill_label = Label(self.master, text = '-' , font = 'Helvetica 11', borderwidth = 1, relief = 'solid')
				kill_label.grid(row = 1, column = i + 1, sticky=W+E+N+S)
				death_label = Label(self.master, text = '-', font = 'Helvetica 11', borderwidth = 1, relief = 'solid')
				death_label.grid(row = 2, column = i + 1, sticky=W+E+N+S)
				kd_label = Label(self.master, text = '-', font = 'Helvetica 11', borderwidth = 1, relief = 'solid')
				kd_label.grid(row = 3, column = i + 1, sticky=W+E+N+S)
				map_played_label = Label(self.master, text = '0', font = 'Helvetica 11', borderwidth = 1, relief = 'solid')
				map_played_label.grid(row = 4, column = i + 1, sticky=W+E+N+S)
				winrate_label = Label(self.master, text = '-', font = 'Helvetica 11', borderwidth = 1, relief = 'solid')
				winrate_label.grid(row = 5, column = i + 1, sticky=W+E+N+S)
				hsp_label = Label(self.master, text = '-', font = 'Helvetica 11', borderwidth = 1, relief = 'solid')
				hsp_label.grid(row = 6, column = i + 1, sticky=W+E+N+S)
				mvp_label = Label(self.master, text = '-', font = 'Helvetica 11', borderwidth = 1, relief = 'solid')
				mvp_label.grid(row = 7, column = i + 1, sticky=W+E+N+S)
				i += 1
			else:
				kill_label = Label(self.master, text = str(round(all_match_stats[key]['Total Kills']/all_match_stats[key]['Matches Played'], 2)) , font = 'Helvetica 11', borderwidth = 1, relief = 'solid')
				kill_label.grid(row = 1, column = i + 1, sticky=W+E+N+S)
				death_label = Label(self.master, text = str(round(all_match_stats[key]['Total Deaths']/all_match_stats[key]['Matches Played'], 2)), font = 'Helvetica 11', borderwidth = 1, relief = 'solid')
				death_label.grid(row = 2, column = i + 1, sticky=W+E+N+S)
				kd_label = Label(self.master, text = str(all_match_stats[key]['KD Ratio']), font = 'Helvetica 11', borderwidth = 1, relief = 'solid')
				kd_label.grid(row = 3, column = i + 1, sticky=W+E+N+S)
				map_played_label = Label(self.master, text = str(all_match_stats[key]['Matches Played']), font = 'Helvetica 11', borderwidth = 1, relief = 'solid')
				map_played_label.grid(row = 4, column = i + 1, sticky=W+E+N+S)
				winrate_label = Label(self.master, text = str(round(all_match_stats[key]['Wins']/all_match_stats[key]['Matches Played'], 2)), font = 'Helvetica 11', borderwidth = 1, relief = 'solid')
				winrate_label.grid(row = 5, column = i + 1, sticky=W+E+N+S)
				hsp_label = Label(self.master, text = str(round(100*all_match_stats[key]['Headshot Kills']/all_match_stats[key]['Total Kills'], 2)), font = 'Helvetica 11', borderwidth = 1, relief = 'solid')
				hsp_label.grid(row = 6, column = i + 1, sticky=W+E+N+S)
				mvp_label = Label(self.master, text =str(round(all_match_stats[key]['MVP Count']/all_match_stats[key]['Matches Played'], 2)), font = 'Helvetica 11', borderwidth = 1, relief = 'solid')
				mvp_label.grid(row = 7, column = i + 1, sticky=W+E+N+S)
				i += 1
		self.button_label = Label(self.master, text = 'Data Visualization Options', bg = '#1A39B1', fg = '#d7e1f2', font = 'Helvetica 11 bold')
		self.button_label.grid(row=8, column = 0, columnspan = 8, sticky=W+E+N+S)

		self.pie_button = Button(self.master, text = 'Pie Chart: Maps Played Distribution', command = lambda: pie_chart_maps_played(all_match_stats),
									 relief = 'raised', borderwidth = 3, bg = '#c4dfe6', fg = '#07575b', font = 'Helvetica 11 bold')
		self.pie_button.grid(row = 9, column = 0, columnspan = 2, sticky=W+E+N+S)

		self.map_win_pct_button = Button(self.master, text = 'Bar Graph: Map Winrate %', command = lambda: bar_graph_maps_win_pct(all_match_stats),
									 relief = 'raised', borderwidth = 3, bg = '#c4dfe6', fg = '#07575b', font = 'Helvetica 11 bold')
		self.map_win_pct_button.grid(row = 9, column = 2, columnspan = 2, sticky=W+E+N+S)

		self.avg_kills_and_deaths_button = Button(self.master, text = 'Bar Graph: Average K-D Per Map', command = lambda: avg_kills_deaths_per_map(all_match_stats),
									 				relief = 'raised', borderwidth = 3, bg = '#c4dfe6', fg = '#07575b', font = 'Helvetica 11 bold')
		self.avg_kills_and_deaths_button.grid(row = 9, column = 4, columnspan = 2, sticky=W+E+N+S)

		self.avg_hsp_button = Button(self.master, text = 'Bar Graph: Average HS % Per Map', command = lambda: avg_hsp_per_map(all_match_stats),
									 				relief = 'raised', borderwidth = 3, bg = '#c4dfe6', fg = '#07575b', font = 'Helvetica 11 bold')
		self.avg_hsp_button.grid(row = 9, column = 6, columnspan = 2, sticky=W+E+N+S)

		self.main_menu_button = Button(self.master, text = 'Back to Main Menu', command = lambda: self.back_to_main_menu(self.master),
									 				relief = 'raised', borderwidth = 3, bg = '#c4dfe6', fg = '#07575b', font = 'Helvetica 11 bold')
		self.main_menu_button.grid(row = 10, column = 0, columnspan = 8, sticky=W+E+N+S)

	def remove_widgets(self):
		for widget in self.master.grid_slaves():
			widget.destroy()


def pie_chart_maps_played(all_match_stats):
	sizes = []
	sorted_label_list = []
	fig1, ax1 = plt.subplots()

	for key in list(all_match_stats.keys()):
		if(all_match_stats[key]['Matches Played'] == '0' or all_match_stats[key]['Matches Played'] == '-'):
			pass
		else:
			sizes.append(all_match_stats[key]['Matches Played'])
			sorted_label_list.append(key)

	ax1.pie(sizes, labels = sorted_label_list, autopct='%1.1f%%')
	ax1.axis('equal')
	plt.title('Maps Played Distribution')
	plt.show()

def bar_graph_maps_win_pct(all_match_stats):
	width = 0.6
	fig, ax = plt.subplots()
	win_pcts = []
	tie_pcts = []
	loss_pcts = []
	labels = []
	for key in list(all_match_stats.keys()):
		if(all_match_stats[key]['Matches Played'] == '0' or all_match_stats[key]['Matches Played'] == '-' ):
			pass
		else:
			win_pcts.append(100 * all_match_stats[key]['Wins']/all_match_stats[key]['Matches Played'])
			tie_pcts.append(100 * all_match_stats[key]['Ties']/all_match_stats[key]['Matches Played'])
			loss_pcts.append(100 * all_match_stats[key]['Losses']/all_match_stats[key]['Matches Played'])
			labels.append(key)

	ind = np.arange(len(labels))
	p1 = plt.bar(ind + width / 2, win_pcts, width, color = 'g')
	p2 = plt.bar(ind + width / 2, tie_pcts, width, bottom = win_pcts, color = 'y')
	p3 = plt.bar(ind + width / 2, loss_pcts, width, bottom = [win_pcts[i] + tie_pcts[i] for i in range(len(win_pcts))], color = 'r')
	#ax.set_xticklabels(labels)
	ax.autoscale_view()
	fig.autofmt_xdate()
	#plt.bar(labels, map_pcts, width = ind_width)
	plt.xticks(ind + width / 2, labels)
	plt.legend((p1[0], p2[0], p3[0]), ('Wins', 'Ties', 'Losses'))
	plt.title('Map Win/Tie/Loss Percentage Comparison')
	plt.xlabel('Maps')
	plt.ylabel('Percentage')
	plt.show()

def avg_kills_deaths_per_map(all_match_stats):
	width = 0.35
	labels_keys = []
	avg_kills = []
	avg_deaths = []
	for key in list(all_match_stats.keys()):
		if(all_match_stats[key]['Matches Played'] == 0 or all_match_stats[key]['Matches Played'] == '-'):
			pass
		else:
			labels_keys.append(key)
			avg_kills.append(all_match_stats[key]['Total Kills']/all_match_stats[key]['Matches Played'])
			avg_deaths.append(all_match_stats[key]['Total Deaths']/all_match_stats[key]['Matches Played'])
	ind = np.arange(len(labels_keys))
	fig, ax = plt.subplots()
	p1 = ax.bar(ind, avg_kills, width, color = 'g')
	p2 = ax.bar(ind + width, avg_deaths, width, color = 'r')
	ax.set_xticks(ind + width / 10)
	ax.set_xticklabels(labels_keys)
	plt.legend((p1[0], p2[0]), ('Kills', 'Deaths'))
	plt.title('Kills vs Deaths Per Map Comparison')
	plt.xlabel('Maps')
	plt.ylabel('Kills or Deaths')
	ax.autoscale_view()
	fig.autofmt_xdate()
	plt.show()

def avg_hsp_per_map(all_match_stats):
	width = 0.6
	fig, ax = plt.subplots()
	hsp_pcts = []
	labels = []
	for key in list(all_match_stats.keys()):
		if(all_match_stats[key]['Matches Played'] == '0' or all_match_stats[key]['Matches Played'] == '-' ):
			pass
		else:
			hsp_pcts.append(100*all_match_stats[key]['Headshot Kills']/all_match_stats[key]['Total Kills'])
			labels.append(key)

	ind = np.arange(len(labels))
	p2 = ax.bar(ind + width / 2, hsp_pcts, width, color = 'b')
	ax.set_xticks(ind + width / 2)
	ax.set_xticklabels(labels)
	ax.autoscale_view()
	fig.autofmt_xdate()
	#plt.bar(labels, map_pcts, width = ind_width)
	plt.title('Map Headshot Percentage Comparison')
	plt.xlabel('Maps')
	plt.ylabel('Headshot Percentage')
	plt.show()



#If maps played count y is 0, then return a string instead of undefined 
def safe_division(x, y):
	if(y == 0):
		return 'Map Not Played'
	else:
		return x/y

#Helper function for KDA Table
def match_info_parser(dict,  match):
	dict['De_' + match.map.strip()]['Total Kills'] += int(match.kills)
	dict['De_' + match.map.strip()]['Total Deaths'] += int(match.deaths)
	dict['De_' + match.map.strip()]['Matches Played'] += 1
	dict['De_' + match.map.strip()]['Headshot Kills'] += round(int(match.kills) * 0.01 * int(match.hsp))
	dict['De_' + match.map.strip()]['MVP Count'] += int(match.mvps)
	dict['De_' + match.map.strip()]['Total Rounds For'] += int(match.rounds_for)
	dict['De_' + match.map.strip()]['Total Rounds Against'] += int(match.rounds_against)
	if(int(match.rounds_for) > int(match.rounds_against)):
		dict['De_' + match.map.strip()]['Wins'] += 1
	elif(int(match.rounds_for) == int(match.rounds_against)):
		dict['De_' + match.map.strip()]['Ties'] += 1
	else:
		dict['De_' + match.map.strip()]['Losses'] += 1

########################################################################################################################################
#  Purpose: Trawls through matches in match_list and gets statistics for each map in the competitive map pool                          #
#  Modifies: Nothing                                                                                                                   #
#  Returns: A dictionary that has keys for each map, which point to a sub-dictionary that has keys for kills, deaths, K-D ratio etc    #
########################################################################################################################################

def kda_table():
	active_duty_map_list = ['Mirage', 'Inferno', 'Nuke', 'Overpass', 'Train', 'Dust II', 'Cache']
	retval = {
		'De_Mirage': {'Total Kills': 0, 'Total Deaths': 0, 'KD Ratio': 0, 'Matches Played': 0, 'Headshot Kills': 0, 'MVP Count': 0, 'Total Rounds For': 0, 'Total Rounds Against': 0, 'Wins': 0, 'Ties': 0, 'Losses': 0},
		'De_Inferno': {'Total Kills': 0, 'Total Deaths': 0, 'KD Ratio': 0, 'Matches Played': 0, 'Headshot Kills': 0, 'MVP Count': 0, 'Total Rounds For': 0, 'Total Rounds Against': 0, 'Wins': 0, 'Ties': 0, 'Losses': 0},
		'De_Nuke': {'Total Kills': 0, 'Total Deaths': 0, 'KD Ratio': 0, 'Matches Played': 0, 'Headshot Kills': 0, 'MVP Count': 0, 'Total Rounds For': 0, 'Total Rounds Against': 0, 'Wins': 0, 'Ties': 0, 'Losses': 0},
		'De_Overpass': {'Total Kills': 0, 'Total Deaths': 0, 'KD Ratio': 0, 'Matches Played': 0, 'Headshot Kills': 0, 'MVP Count': 0,  'Total Rounds For': 0, 'Total Rounds Against': 0, 'Wins': 0, 'Ties': 0, 'Losses': 0},
		'De_Train': {'Total Kills': 0, 'Total Deaths': 0, 'KD Ratio': 0, 'Matches Played': 0, 'Headshot Kills': 0, 'MVP Count': 0, 'Total Rounds For': 0, 'Total Rounds Against': 0, 'Wins': 0, 'Ties': 0, 'Losses': 0},
		'De_Dust II': {'Total Kills': 0, 'Total Deaths': 0, 'KD Ratio': 0, 'Matches Played': 0, 'Headshot Kills': 0, 'MVP Count': 0, 'Total Rounds For': 0, 'Total Rounds Against': 0, 'Wins': 0, 'Ties': 0, 'Losses': 0},
		'De_Cache': {'Total Kills': 0, 'Total Deaths': 0, 'KD Ratio': 0, 'Matches Played': 0, 'Headshot Kills': 0, 'MVP Count': 0, 'Total Rounds For': 0, 'Total Rounds Against': 0, 'Wins': 0, 'Ties': 0, 'Losses': 0},
	}

	for match in match_list:
		if(match.map.strip() not in active_duty_map_list):
			pass
		else:
			match_info_parser(retval, match)

	for map_name in list(retval.keys()):
		if(retval[map_name]['Matches Played'] == 0):
			for key in list(retval[map_name].keys()):
				retval[map_name][key] = '-'
		else:
			if(retval[map_name]['Total Deaths'] == 0):
				retval[map_name]['KD Ratio'] = 'Undefined'
			else:
				retval[map_name]['KD Ratio'] = round(retval[map_name]['Total Kills']/retval[map_name]['Total Deaths'], 2)	
	return retval


if __name__ == '__main__':
	freeze_support()
	global file_name
	root = Tk()
	test_gui = CSV_File_Submit_GUI(root)
	root.mainloop()


