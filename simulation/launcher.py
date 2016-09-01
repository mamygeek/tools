# lance simulations pour different nombre d'electeurs
import multiprocessing
import mj
import os, sys
import shutil
import time
import numpy as np

def worker((Ncandidats,Nelecteurs, Nlot, Nmentions, root, output, id)):
    """worker function"""
    sys.stdout.write('\nSTART -- %i candidats, %i electeurs, %i ID, %i PID -- \n' %  \
                    (Ncandidats, Nelecteurs, id, os.getpid()))
    sys.stdout.flush()
    time.sleep(0.01) # being sure that simulation are differently initialized
    o = open(output, "w")
    mj.simulation(Ncandidats,Nelecteurs, Nlot, Nmentions, root,o,0)
    o.close()
    sys.stdout.write('\nDONE -- %i candidats, %i electeurs, %i PID -- \n' %  \
                    (Ncandidats, Nelecteurs, os.getpid()))
    sys.stdout.flush()
    return

if __name__ == '__main__':
    print "Cette fois, c'est la bonne !"
    print (time.strftime("%H:%M:%S"))
    
    root = "Nmin/"
    try:
        os.mkdir(root)
    except OSError:
        pass
        
    Nelecteurs = 100000
    electeurs  = np.arange(10000, Nelecteurs,1000)
    sizeE      = len(electeurs)
    sizeC      = 1
    Ncandidats = 16#np.arange(50,110,10)
    candidats  = [Ncandidats]
    Nlot       = 5
    Nmentions  = 5
    Ntest      = 5 # chaque Nelecteurs est teste Ntest fois
    Nworkers   = Ntest*sizeE*sizeC
    data       = "scripts/terranova.txt"
    args       = []
    for i in range(sizeC):
        for j in range(sizeE):
            for t in range(Ntest):
                
                c = candidats[i]
                e = electeurs[j]
                folder = root + "C_%i.E_%i_%i/" % (c,e,t)
                #shutil.rmtree(folder, True)
                try:
                    os.mkdir(folder)
                    shutil.copy(data, folder)
                    f = folder + "log.txt"
                    id = (i+1)*(j+1)*(t+1)+(j+1)*(t+1)+t
                    arg = [c,e,Nlot,Nmentions,folder,f,id]
                    args.append(arg)
                except OSError:
                   pass
                
    if args == []:
        print "Rien a faire!"
    pool       = multiprocessing.Pool()
    pool.map(worker, args)
                
    print "Alors, ca marche ? :)"
        


