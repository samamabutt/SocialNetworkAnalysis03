# -- coding: utf-8 --
"""
Created on Sat Mar 30 05:31:40 2019

@author: Samama
"""



import snap

import matplotlib.pyplot as plt

karate = snap.LoadEdgeList(snap.PUNGraph, "karateclub.txt", 0, 1)




def getModularity(subG):
    
    if karate.GetEdges > 0:
        
        #twoM = karate.GetEdges()
        
        sumO = float(0.0)
        
        
        
        for node1 in subG.Nodes():
            
            for node2 in subG.Nodes():
                #change
                expec = float(float(karate.GetNI(node1.GetId()).GetOutDeg()) * float(karate.GetNI(node2.GetId()).GetOutDeg()))
                #change
                expec = float(float(expec)/normalz)
                
                
                aij  = 0.0
                #change
                if (karate.IsEdge(node1.GetId(),node2.GetId())):
                    
                    aij = 1.0 
                    
                expec = float(aij - expec)
                
                sumO = sumO + expec
                
        return sumO

    else:
        
        return 0


modularity = []

count = 0

mod = 0
       
normalz = 2 * karate.GetEdges()

while(karate.GetEdges() > 0):     
     
    edge_betweenness = []
    
    Nodes = snap.TIntFltH()
    
    Edges = snap.TIntPrFltH()
    
    snap.GetBetweennessCentr(karate, Nodes, Edges, 1.0)

    
    
    
    
    
    
    
    
#    for edge in Edges:
#        
#        print "edge: (%d, %d) betweeness: %f" % (edge.GetVal1(), edge.GetVal2(), Edges[edge])
     
    for edge in Edges:
        
        edge_betweenness.append(Edges[edge])
        
    
    # print "edge: (%d, %d) centrality: %f" % (edge.GetVal1(), edge.GetVal2(), Edges[edge])
    
    edge_betweenness.sort(reverse=True)
    
    subGraphs = []
    
    verified = []
    
    community = []
    
    
    for edge in Edges: 
           
        if (Edges[edge] == edge_betweenness[0]):
        

            karate.DelEdge(edge.GetVal1(), edge.GetVal2())
                
          
            BfsTree1 = snap.GetBfsTree(karate, edge.GetVal1(), True, False)
            
            BfsTree2 = snap.GetBfsTree(karate, edge.GetVal2(), True, False)
            
            NIdV1 = snap.TIntV()
            
            NIdV2 = snap.TIntV()
            
            if (edge.GetVal1() not in verified):
                
                for nodes in BfsTree1.Nodes():
                    
                    NIdV1.Add(nodes.GetId())
                    
                subGraphs.append(snap.GetSubGraph(karate, NIdV1))
                
            if (edge.GetVal2() not in verified):
                
                for nodes in BfsTree2.Nodes():
                    
                    NIdV2.Add(nodes.GetId())
                    
                subGraphs.append(snap.GetSubGraph(karate, NIdV2))
            
            verified.append(edge.GetVal1())
            
            verified.append(edge.GetVal2())
        
        
        
    normalz = 2 * karate.GetEdges()
    
    modularityQ = float(0.0)
    
    
    if normalz > 0:
        
        for graphs in subGraphs:
            
            modularityQ = modularityQ + getModularity(graphs)
        
        modularityQ = float(float(modularityQ)/float(normalz))
        
        if modularityQ > mod:
        
            mod = modularityQ
            
#            community = subGraphs[graphs]
            
        
    modularity.append((count,modularityQ))
    
    
    
    count = count + 1   
    
    
    
    
#    print "Nodes", node1 ,"and", node2, "Betweeness", betweeness
#    
#    print "Total Edges", karate.GetEdges()
#            
#    print "Modularity = ",modularityQ
    

            


#print(modularity) 

print "Highest Modularity:", mod  

#print "Community", community

counts_array = []
    
mod_array = []

for element in modularity:
    ind, mod = element
    counts_array.append(ind)
    mod_array.append(mod)        
   
plt.plot(counts_array, mod_array)
plt.xlabel('iteration')
plt.ylabel('Modularity')
plt.show()