import subprocess
import time

known_window_ids = []
temporary_window_ids = []

template = "xprop -f _KDE_NET_WM_BLUR_BEHIND_REGION 32c -set _KDE_NET_WM_BLUR_BEHIND_REGION 0 -id "

def get_window_ids(get_open=False):
	output = subprocess.run(["wmctrl","-l"], stdout=subprocess.PIPE).stdout.decode()
	id_buffer=""
	reading = True
	open_windows = []
	for character in output:
		if character != " " and reading:
			id_buffer += character
		
		else:
			reading =  False
			if character == "\n":
				if id_buffer not in temporary_window_ids:
					temporary_window_ids.append(id_buffer)
				id_buffer = ""
				reading = True
	
	#Window closed
	for kid in known_window_ids:
		if kid not in temporary_window_ids:
			known_window_ids.remove(kid)
			
	#Window opened
	for tid in temporary_window_ids:
		if tid not in known_window_ids:
			known_window_ids.append(tid)
			if get_open:
				open_windows.append(tid)
	temporary_window_ids.clear()
	
	if get_open:
		return open_windows
	
	
	
def blur(wid):
	x = list(template.split())
	x.append(wid)
	subprocess.run(x)
	x.clear()
	
	
	
while True:
	time.sleep(0.1)
	delta = get_window_ids(True)
	if len(delta) > 0:
		for window_id in delta:
			blur(window_id)