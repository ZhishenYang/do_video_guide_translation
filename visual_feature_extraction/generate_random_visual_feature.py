import numpy as np
import os
import argparse 
from tqdm import tqdm 
#Dim feature extracted from Resnet-152 average pool
#1*10*2048

#Dim feature extracted from Resnet-152 relu 
#1*10*1024*14*14

#a = np.full((1,10,2048),0)

def generate_random_initialized_visual_features(input_path, output_path)->None:

    for split in ['train', 'valid', 'test']:
        list_of_visual_features = os.listdir(os.path.join(input_path, split))
        print(f"Number of visual features in {split}: {len(list_of_visual_features)}")
        os.mkdir(os.path.join(output_path, split))
    
        for visual_feature in tqdm(list_of_visual_features):
            f = open(os.path.join(output_path, split, visual_feature.strip('.npy')), 'wb')

            if ('avgpool' in visual_feature):
                np.save(f, np.random.rand(1,10,2048))

            if ('res4frelu' in visual_feature):
                #np.save(f, np.full((1,10,1024,14,14),0.1))
                np.save(f, np.random.rand(1,10,1024,14,14))
            
            f.close()

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(prog='Generate visual features random ')

    parser.add_argument('-i', '--input-path', type=str, required=True,
                        help='Input path to directory that contains extracted visual features')

    parser.add_argument('-o','--output-path', type=str, required=True,
                        help='Output path to directory that saves random initialized visual features')
    
    args = parser.parse_args()

    print(f"Input path: {args.input_path}")
    print(f"Input path: {args.output_path}")

    generate_random_initialized_visual_features(args.input_path, args.output_path)

    #1. Read a list of file names 
    #2. create a new directory 
    #3. Save random initialed visaul features into that directory with prope file names 

