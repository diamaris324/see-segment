
"""File RunSearch.py, runs genetic search continuously."""

import argparse
import sys
import matplotlib.pylab as plt
import imageio
from see import GeneticSearch, Segmentors
import random


from see.Segmentors import segmentor
from see.ColorSpace import colorspace
from see.Workflow import workflow
from see.Segment_Fitness import segment_fitness
from see import base_classes 
from see.git_version import git_version
<<<<<<< HEAD
=======

def write_algo_vector(fpop_file, outstring):
    """Write list of algorithm parameters to string."""
    with open(fpop_file, 'a') as myfile:
        myfile.write(f'{outstring}\n')
        
def read_algo_vector(fpop_file):
    """Create list of algorithm parameters for each iteration."""
    inlist = []
    with open(fpop_file,'r') as myfile:
        for line in myfile:
            inlist.append(eval(line))
    return inlist
>>>>>>> nate-docs2
    
def continuous_search(input_file, 
                      input_mask, 
                      startfile=None,
                      checkpoint='checkpoint.txt',
                      best_mask_file="temp_mask.png", 
                      pop_size=10):
    """Run genetic search continuously.
    
    input_file: the original image
    input_mask: the ground truth mask for the image
    pop_size: the size of the population
    Runs indefinitely unless a perfect value (0.0) is reached.
    """
    mydata = base_classes.pipedata()
    mydata.img = imageio.imread(input_file)
    mydata.gmask = imageio.imread(input_mask)

    outfile=f"{input_file}.txt"
    
    #TODO: Read this file in and set population first
    workflow.addalgos([colorspace, segmentor, segment_fitness])
    wf = workflow()
    
    #Run the search
    my_evolver = GeneticSearch.Evolver(workflow, mydata, pop_size=pop_size)

    best_fitness=2.0
    iteration = 0
 
    while(best_fitness > 0.0):
        print(f"running {iteration} iteration")
        if(startfile):
            population = my_evolver.run(ngen=1, startfile=startfile)
        else:
            population = my_evolver.run(ngen=1)
            
        #Get the best algorithm so far
        params = my_evolver.hof[0]

        #Generate mask of best so far.
        seg = workflow(paramlist=params)
        mydata = seg.pipe(mydata)
        
        fitness = mydata.fitness
        if (fitness < best_fitness):
            best_fitness = fitness
            print(f"\n\n\n\nIteration {iteration} Finess Improved to {fitness}")
            my_evolver.writepop(population, filename="checkpoint.pop")
            imageio.imwrite(best_mask_file,mydata.mask);
            GeneticSearch.write_algo_vector(fpop_file, f"[{iteration}, {fitness}, {params}]\n") 
            ###TODO Output [fitness, seg]
        iteration += 1

def geneticsearch_commandline():
    """Rename Instructor notebook using git.
    
    Fix all student links in files.
    """
    parser = argparse.ArgumentParser(description='Run Genetic Search on Workflow')

    parser.add_argument('input_file', help=' input image')
    parser.add_argument('input_mask', help=' input Ground Truthe Mask')
    parser.add_argument('start_pop', nargs='?', help=' Population File used in transfer learning')
    parser.add_argument('--seed', type=int,default=1, help='Input seed (integer)') 
    args = parser.parse_args()
    
    print('\n\n')
    print(args)
    print('\n\n')
    
    #TODO: add this to the setup.py installer so we include the has in the install. 
    print(f"Current Git HASH: {git_version()}")
    
    random.seed(args.seed)
    
    continuous_search(args.input_file, args.input_mask, args.start_pop);

#     #Multilabel Array Example
#     img = imageio.imread(args.input_file)
#     gmask = imageio.imread(args.input_mask)

#     #Run the search
#     my_evolver = GeneticSearch.Evolver(img, gmask, pop_size=10)
#     population = my_evolver.run(ngen=5)
    
#     #Get the best algorithm so far
#     params = my_evolver.hof[0]
#     print('Best Individual:\n', params)
    
#     #Generate mask of best so far.
#     seg = Segmentors.algoFromParams(params)
#     mask = seg.evaluate(img)
    
#     imageio.imwrite('./temp_mask.png',mask);
    
    
if __name__ == "__main__":
    geneticsearch_commandline()
