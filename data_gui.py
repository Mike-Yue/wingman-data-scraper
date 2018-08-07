import matplotlib.pyplot as plt
import csv
import numpy as np
from decimal import Decimal
import threading
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from multiprocessing import freeze_support
import os

match_list = []

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

def pie_chart_maps_played():
	labels = ['De_Mirage', 'De_Inferno', 'De_Nuke', 'De_Overpass', 'De_Train', 'De_Dust2', 'De_Cache']
	mirage, inferno, nuke, overpass, train, dust2, cache = 0, 0, 0, 0, 0, 0, 0
	for match in match_list:
		if(match.map.strip() == 'Mirage'):
			mirage += 1
		elif(match.map.strip() == 'Inferno'):
			inferno += 1
		elif(match.map.strip() == 'Nuke'):
			nuke += 1
		elif(match.map.strip() == 'Overpass'):
			overpass += 1
		elif(match.map.strip() == 'Train'):
			train += 1
		elif(match.map.strip() == 'Dust II'):
			dust2 += 1
		elif(match.map.strip() == 'Cache'):
			cache += 1
		else:
			pass
	sizes = [mirage, inferno, nuke, overpass, train, dust2, cache]
	fig1, ax1 = plt.subplots()
	ax1.pie(sizes, labels = labels, autopct='%1.1f%%')
	ax1.axis('equal')
	plt.show()

def bar_graph_maps_played_vs_win_pct():
	labels = ['De_Mirage', 'De_Inferno', 'De_Nuke', 'De_Overpass', 'De_Train', 'De_Dust2', 'De_Cache']
	mirage, inferno, nuke, overpass, train, dust2, cache = 0, 0, 0, 0, 0, 0, 0
	mirage_win, inferno_win, nuke_win, overpass_win, train_win, dust2_win, cache_win = 0, 0, 0, 0, 0, 0, 0

	width = 0.6
	ind = np.arange(7)
	for match in match_list:
		if(match.map.strip() == 'Mirage'):
			mirage += 1
			if(int(match.rounds_for) > int(match.rounds_against)):
				mirage_win += 1
		elif(match.map.strip() == 'Inferno'):
			inferno += 1
			if(int(match.rounds_for) > int(match.rounds_against)):
				inferno_win += 1
		elif(match.map.strip() == 'Nuke'):
			nuke += 1
			if(int(match.rounds_for) > int(match.rounds_against)):
				nuke_win += 1
		elif(match.map.strip() == 'Overpass'):
			overpass += 1
			if(int(match.rounds_for) > int(match.rounds_against)):
				overpass_win += 1
		elif(match.map.strip() == 'Train'):
			train += 1
			if(int(match.rounds_for) > int(match.rounds_against)):
				train_win += 1
		elif(match.map.strip() == 'Dust II'):
			dust2 += 1
			if(int(match.rounds_for) > int(match.rounds_against)):
				dust2_win += 1
		elif(match.map.strip() == 'Cache'):
			cache += 1
			if(int(match.rounds_for) > int(match.rounds_against)):
				cache_win += 1
		else:
			pass
	fig, ax = plt.subplots()
	win_pcts = [100*mirage_win/mirage, 100*inferno_win/inferno, 100*nuke_win/nuke, 100*overpass_win/overpass, 100*train_win/train, 100*dust2_win/dust2, 100*cache_win/cache]
	p2 = ax.bar(ind + width / 2, win_pcts, width, color = 'b')
	ax.set_xticks(ind + width / 2)
	ax.set_xticklabels(labels)
	ax.autoscale_view()
	fig.autofmt_xdate()
	#plt.bar(labels, map_pcts, width = ind_width)
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

	avg_kills = [mirage_kills/mirage, inferno_kills/inferno, nuke_kills/nuke, overpass_kills/overpass, train_kills/train, dust2_kills/dust2, cache_kills/cache]
	avg_deaths = [mirage_deaths/mirage, inferno_deaths/inferno, nuke_deaths/nuke, overpass_deaths/overpass, train_deaths/train, dust2_deaths/dust2, cache_deaths/cache]
	for i in range(0, len(avg_deaths)):
		map_kda = Decimal(avg_kills[i]/avg_deaths[i])
		map_kda = round(map_kda, 2)
		kda.append(map_kda)
		avg_kills[i] = round(Decimal(avg_kills[i]), 2)
		avg_deaths[i] = round(Decimal(avg_deaths[i]), 2)
	retval.append(avg_kills)
	retval.append(avg_deaths)
	retval.append(kda)
	return retval


def browse():
	global csv_entry_menu, file
	csv_entry_menu.filename = filedialog.askopenfilename(initialdir = "/", title = "Select file", filetypes = (("csv files (.csv)","*.csv"),("all files","*.*")))
	file.delete(0,END)
	file.insert(0,csv_entry_menu.filename)

def read_file():
	global file, match_list, file_name
	file_name = file.get()

	try:
		with open(file_name, 'r') as data_file:
			csv_data = csv.reader(data_file)
			next(csv_data)
			for row in csv_data:
				match = Match(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14])
				match_list.append(match)
			csv_entry_menu.destroy()

	except (IOError, FileNotFoundError) as e:
		file_name = None
		print(e)

if __name__ == '__main__':
	freeze_support()
	global file_name
	csv_entry_menu = tkinter.Tk()
	csv_entry_menu.title("Submit Your CSV Data File")
	csv_entry_menu.geometry("700x105")
	csv_entry_menu.resizable(False, False)

	csv_entry_menu.rowconfigure(0, weight = 2)
	csv_entry_menu.rowconfigure(1, weight = 1)
	csv_entry_menu.rowconfigure(2, weight = 2)
	csv_entry_menu.columnconfigure(0, weight = 1)
	csv_entry_menu.columnconfigure(1, weight = 1)


	csv_caption = Label(csv_entry_menu, text = 'Select your csv file by either typing in the path or using Browse Files', bg = '#003b46', fg = '#d7e1f2', font = 'Helvetica 11 bold')
	csv_caption.grid(row = 0, column = 0, columnspan = 2, sticky=W+E+N+S)


	file = Entry(csv_entry_menu, font = 'Helvetica 10', bd = 4)
	file.grid(row = 1, column = 0, columnspan = 2, ipady = 2, ipadx = 2, sticky=W+E+N+S)

	browse_files = tkinter.Button(csv_entry_menu, text = 'Browse Files', command = browse,
								  relief = 'ridge', borderwidth = 3, bg = '#c4dfe6', fg = '#07575b', font = 'Helvetica 11 bold')
	browse_files.grid(row = 2, column = 0, columnspan = 1, sticky=W+E+N+S)

	submit_file = tkinter.Button(csv_entry_menu, text = 'Submit File', command = read_file,
								 relief = 'ridge', borderwidth = 3, bg = '#c4dfe6', fg = '#07575b', font = 'Helvetica 11 bold')
	submit_file.grid(row = 2, column = 1, columnspan = 1, sticky=W+E+N+S)

	csv_entry_menu.mainloop()

	try:
		file_name
	except NameError:
		os._exit(-1)
	if(file_name == None):
		os._exit(-1)

	action_menu = tkinter.Tk()
	action_menu.title("View Your Stats")
	action_menu.geometry("1280x720")
	action_menu.resizable(False, False)

	for rows in range(0, 4):
		action_menu.rowconfigure(rows, weight = 1)
	for cols in range(0, 8):
		action_menu.columnconfigure(cols, weight = 1)

	mirage_label = Label(action_menu, text = 'De_Mirage', bg = '#003b46', fg = '#d7e1f2', font = 'Helvetica 11 bold')
	mirage_label.grid(row = 0,  column = 1, sticky=W+E+N+S)
	inferno_label = Label(action_menu, text = 'De_Inferno', bg = '#003b46', fg = '#d7e1f2', font = 'Helvetica 11 bold')
	inferno_label.grid(row = 0,  column = 2, sticky=W+E+N+S)
	nuke_label = Label(action_menu, text = 'De_Nuke', bg = '#003b46', fg = '#d7e1f2', font = 'Helvetica 11 bold')
	nuke_label.grid(row = 0,  column = 3, sticky=W+E+N+S)
	overpass_label = Label(action_menu, text = 'De_Overpass', bg = '#003b46', fg = '#d7e1f2', font = 'Helvetica 11 bold')
	overpass_label.grid(row = 0,  column = 4, sticky=W+E+N+S)
	train_label = Label(action_menu, text = 'De_Train', bg = '#003b46', fg = '#d7e1f2', font = 'Helvetica 11 bold')
	train_label.grid(row = 0,  column = 5, sticky=W+E+N+S)
	dust2_label = Label(action_menu, text = 'De_Dust2', bg = '#003b46', fg = '#d7e1f2', font = 'Helvetica 11 bold')
	dust2_label.grid(row = 0,  column = 6, sticky=W+E+N+S)
	cache_label = Label(action_menu, text = 'De_Cache', bg = '#003b46', fg = '#d7e1f2', font = 'Helvetica 11 bold')
	cache_label.grid(row = 0, columnspan = 5, column = 7, sticky=W+E+N+S)
	kills_lable = Label(action_menu, text = 'Kills', bg = '#003b46', fg = '#d7e1f2', font = 'Helvetica 11 bold')
	kills_lable.grid(row = 1, column = 0, sticky = W+E+N+S)
	deaths_lable = Label(action_menu, text = 'Deaths', bg = '#003b46', fg = '#d7e1f2', font = 'Helvetica 11 bold')
	deaths_lable.grid(row = 2, column = 0, sticky = W+E+N+S)
	kda_lable = Label(action_menu, text = 'K-D Ratio', bg = '#003b46', fg = '#d7e1f2', font = 'Helvetica 11 bold')
	kda_lable.grid(row = 3, column = 0, sticky = W+E+N+S)

	kda_stats = kda_table()
	for i in range(0, len(kda_stats[0])):
		kill_label = Label(action_menu, text = kda_stats[0][i])
		kill_label.grid(row = 1, column = i + 1)
		death_label = Label(action_menu, text = kda_stats[1][i])
		death_label.grid(row = 2, column = i + 1)
		kd_label = Label(action_menu, text = kda_stats[2][i])
		kd_label.grid(row = 3, column = i + 1)
	#test_lable.grid(row = 0, column = 12)

	action_menu.mainloop()
		#avg_kills_deaths_per_map()
		#pie_chart_maps_played()
		#bar_graph_maps_played_vs_win_pct()


