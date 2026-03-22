import matplotlib.pyplot as plt


lenght = 100
cycles = 100

log = []
cells = [0 for i in range(lenght)]

tempCells = [0 for i in range(lenght)]

#cells[54] = 1
#cells[30] = 1
cells[50] = 1
#cells[60] = 1


#ShowHeatMap
def heatMap(arr):
    plt.imshow( arr )
    plt.show()



print(cells)
log.append(cells)

for cycle in range(cycles):
    
    for idx, cell in enumerate(cells):
    
        count = 0
        
        # go through surrounding
        for j in range(-2, 3):

            lookAt = 0
            
            if j != 0:
            
                # look around the cells list, else look at the surrounding idxs
                if idx + j < 0:
                    lookAt = len(cells) -1 +j
                elif (idx + j) > (len(cells) -1):
                    lookAt = j
                else:
                    lookAt = idx + j
                
                
                if cells[lookAt] == 1:
                    count +=1
        
        
        if cell == 1:

            # rules of survival
            if count == 1:
                tempCells[idx] = 1
            else:
                tempCells[idx] = 0
    
        else:
            # rules of born
            if count == 1:
                tempCells[idx] = 1
        
        print(idx, cell, count)
        
    cells = tempCells.copy()
    
    print(cells)
    
    log.append(cells)
    

heatMap(log)