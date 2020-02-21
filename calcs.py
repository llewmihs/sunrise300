vid_length = 60
fps = 15

frames_req = vid_length * fps

real_time = 60 * 60

time_delay = real_time / frames_req

print(time_delay)