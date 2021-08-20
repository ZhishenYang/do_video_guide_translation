import numpy as np
import os
import argparse 
import sys
from multiprocessing import Pool
import multiprocessing as mp
from itertools import product
#scene: 
#Two types of scenes: 
# first, key frames, last frames
# first, middle frames, and last frames

#Dim feature extracted from Resnet-152 average pool
#1*10*2048

#Dim feature extracted from Resnet-152 relu 
#1*10*1024*14*14

def generate_scene_features(list_of_visual_features, input_per_second_frame, input_key_frame, outpout, task)->None:
    print(task)
    for visual_feature_file in list_of_visual_features:
        if 'avgpool' in visual_feature_file:
            per_second_path = os.path.join(input_per_second_frame, visual_feature_file)
            print(per_second_path)
            
            if task == 'key_frames':                
                key_frame_path = os.path.join(input_key_frame, visual_feature_file) 
            
                # if extracted visual features from key frames exist                  
                if (os.path.exists(key_frame_path)):
                # first frame and last frame and key frames in between 
                    key_frames = np.load(key_frame_path)
                    per_second_frames = np.load(per_second_path)
                    print(f"Per second frames: {per_second_frames.shape}")
                    print(f"Key frames: {key_frames.shape}")
                    '''
                    print("key_frame")
                    print(key_frames)
                    print("Per_second_frames")
                    print(per_second_frames)
                    '''
                    
                    first_frame = per_second_frames[0][0]  
                    last_frame = per_second_frames[0][-1]
                    
                    '''
                    print("first_frame")
                    print(first_frame)
                    print("last_frames")
                    print(last_frame)
                    '''
                    key_frame_scene = np.concatenate(([first_frame], key_frames[0], [last_frame]))
                    key_frame_scene = key_frame_scene[np.newaxis, : ]
                    print(f"Key frame scene: {key_frame_scene.shape}")
                    assert(np.array_equal(key_frame_scene[0][0], first_frame))
                    assert(np.array_equal(key_frame_scene[0][-1], last_frame))
                    assert(np.array_equal(key_frame_scene[0][1:-1], key_frames[0]))
                    np.save(os.path.join(output_path, visual_feature_file.strip('.npy')), key_frame_scene)

                else:
                    per_second_frames = np.load(per_second_path)
                    print(f"Per second frames: {per_second_frames.shape}")
                    
                    first_frame = per_second_frames[0][0]  
                    last_frame = per_second_frames[0][-1]
                    

                    key_frame_scene = np.concatenate(([first_frame], [last_frame]))
                    key_frame_scene = key_frame_scene[np.newaxis, : ]
                    print(f"Key frame scene: {key_frame_scene.shape}")
                    assert(np.array_equal(key_frame_scene[0][0], first_frame))
                    assert(np.array_equal(key_frame_scene[0][-1], last_frame))
                    
                    np.save(os.path.join(output_path, visual_feature_file.strip('.npy')), key_frame_scene)  
                
            elif task == "three_frames":
                per_second_frames = np.load(per_second_path)
                        
                first_frame = per_second_frames[0][0]  
                last_frame = per_second_frames[0][-1]
                
                middle_frame_index = int(per_second_frames.shape[1]/2)
                middle_frame = per_second_frames[0][middle_frame_index]
                '''
                print("first_frame")
                print(first_frame)
                print("last_frames")
                print(last_frame)
                print("Middle frame index")
                print(middle_frame_index)
                '''
                three_frame_scene = np.concatenate(([first_frame], [middle_frame], [last_frame]))
                three_frame_scene = three_frame_scene[np.newaxis, : ]
                print(f"Three frame scene: {three_frame_scene.shape}")
                assert(np.array_equal(three_frame_scene[0][0], first_frame))
                assert(np.array_equal(three_frame_scene[0][1], middle_frame))
                assert(np.array_equal(three_frame_scene[0][-1], last_frame))
                '''
                print("_frames")
                print(three_frame_scene)     
                print(output_path)      
                '''
                np.save(os.path.join(output_path, visual_feature_file.strip('.npy')), three_frame_scene) 
            
            elif task == 'single_frame':
                per_second_frames = np.load(per_second_path)                
                middle_frame_index = int(per_second_frames.shape[1]/2)
                '''
                print("first_frame")
                print(first_frame)
                print("last_frames")
                print(last_frame)
                print("Middle frame index")
                print(middle_frame_index)
                '''
                single_frame_scene = per_second_frames[0][middle_frame_index]
                single_frame_scene = single_frame_scene[np.newaxis, np.newaxis, :]
                print(f"Three frame scene: {single_frame_scene.shape}")
                
                assert(np.array_equal(single_frame_scene[0][0], per_second_frames[0][middle_frame_index]))
                '''
                print("_frames")
                print(three_frame_scene)     
                print(output_path)      
                '''
                np.save(os.path.join(output_path, visual_feature_file.strip('.npy')), single_frame_scene) 
                    
if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='Generate scene features')

    parser.add_argument('-k','--input-per-second-frame', type=str, required=True, 
                        help='Input path contains visual features (per_second_frames and keyframes)')

    parser.add_argument('-p','--input-key-frame', type=str, required=True, 
                        help='Input path contains visual features (per_second_frames and keyframes)')
    
    parser.add_argument('-o','--output', type=str, required=True, 
                        help='Output path to save scene features')
                            
    parser.add_argument('-t', '--task', type=str, required=True, 
                        choices=['key_frames', 'three_frames','single_frame'],
                        help='Option: key_frames: first, key frames, last frames. three_frames: first, middle frames, and last frames, single_frame: middle of the frames')

    args = parser.parse_args()

    for split in ['train', 'valid', 'test']:
        
        list_of_per_second_frame_visual_features = os.listdir(os.path.join(args.input_per_second_frame, split))
        output_path = os.path.join(args.output, split)
        print(f"Split: {split}, number of visual features {len(list_of_per_second_frame_visual_features)}")
        
        if (not os.path.isdir(output_path)):
            os.mkdir(output_path)
        input_path = os.path.join(args.input_per_second_frame, split)
        input_key_path = os.path.join(args.input_key_frame, split)
        generate_scene_features(list_of_per_second_frame_visual_features, input_path, input_key_path, output_path, args.task)
        #pool = Pool(processes=2)
        
        #pool.map(generate_scene_features, product(list_of_per_second_frame_visual_features, input_path, input_key_path, output_path, args.task))
        #pool.terminate()
    
