import os
from multiprocessing import Pool
import multiprocessing as mp
from itertools import product
import argparse

# videos are the folder that contains the videos
# subfolder: valid, train, test

def extract_all_frames(option, vid_path, vid_dir, save_dir_path):

	save_dir_path = os.path.join(save_dir_path, vid_path[:-len('.mp4')] if vid_path.endswith('.mp4') else None)

	if not os.path.isdir(save_dir_path):
		os.mkdir(save_dir_path)

	if option == 'key_frames':
		#Extract key frames from a video. #  "select='eq(pict_type,PICT_TYPE_I)'" -vsync vfr
		
		cmd = ['ffmpeg', '-threads 1', '-hide_banner', '-i', os.path.join(vid_dir, vid_path), '-f', 'image2', '-vf', "\"select='eq(pict_type,PICT_TYPE_I)'\"", '-vsync', 'vfr', os.path.join(save_dir_path, '%d.png')]

	elif option == 'per_second_frames': 
		cmd = ['ffmpeg', '-threads 1', '-hide_banner', '-i', os.path.join(vid_dir, vid_path), '-f', 'image2', '-vf', 'fps=1', os.path.join(save_dir_path, '%d.png')]
	
	elif option == 'all_frames':# -vsync vfr
		cmd = ['ffmpeg', '-threads 1', '-hide_banner', '-i', os.path.join(vid_dir, vid_path), '-f', 'image2', '-vsync', 'vfr', os.path.join(save_dir_path, '%d.png')]
	
	elif 'scene_change_frames': #"select='gt(scene,0.5)',metadata=print:file=time.txt"
		cmd = ['ffmpeg', '-threads 1', '-hide_banner', '-i', os.path.join(vid_dir, vid_path), '-f', 'image2', '-vf', "\"select='gt(scene,0.3)'\"", '-vsync', 'vfr', os.path.join(save_dir_path, '%d.png')]
	
	cmd = " ".join(cmd)
	os.system(cmd)
 
def process_videos(vid_dir_path, save_dir_path, option):
	vid_list = os.listdir(vid_dir_path)

	pool = Pool(processes=mp.cpu_count())
	pool.starmap(extract_all_frames, product([option], vid_list, [vid_dir_path], [save_dir_path]))
	pool.terminate()

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Extract per-second frames from each video")
	parser.add_argument("--path", default="", help="Path to the directory that contains video")
	parser.add_argument("--save_path", default="", help="Path to the directory that saves the extracted frames, sub-directory: train/, valid/, and test/")
	parser.add_argument("--option", default="key_frames or per_second_frames or all_frames or scene_change_frames", help="")

	arguments = parser.parse_args()

	# Make folders for saving frames
	save_path_for_frames = os.path.join(arguments.save_path, arguments.option)
	
	if not os.path.isdir(save_path_for_frames):
		os.mkdir(save_path_for_frames)

	for split in ['train', 'test', 'valid']:
		if not os.path.isdir(os.path.join(save_path_for_frames, split)):
			os.mkdir(os.path.join(save_path_for_frames, split))

		vid_dir_path = os.path.join(arguments.path, split)
		save_dir_path = os.path.join(save_path_for_frames, split)
		
		process_videos(vid_dir_path, save_dir_path, arguments.option)