## Median Filter by BBoDDo_lab ##

# Only 2D gray scale images

# %matplotlib notebook
# import numpy as np
# import cv2
# import matplotlib
# from matplotlib import pyplot as plt

def medfilt(A, n):

    # A : input gray sacle image
    # n : n x n filter size
    
    n = round(n)
    if (n + 1) % 2 != 0:
        n = n + 1
    
    A_mf = A.copy()
    
    nn = (n-1)//2
    [row, col] = A.shape 
    
    ar = np.zeros((n,n))
    
    if v == 0:
        for r in range(row):
            for c in range(col):
                for j in range(-nn, nn + 1):
                    for k in range(-nn, nn + 1):
                        if r+j <= -1 or r+j >= row or c+j <= -1 or c+j >= row or r+k <= -1 or r+k >= row or c+k <= -1 or c+k >= row:
                            ar[j+1][k+1] = 0
                        else:
                            ar[j+1][k+1] = A[r+j][c+k]

                arr = np.sort(np.array(ar).ravel())
                A_mf[r][c] = arr[len(arr)//2]
                
    elif v == 1:
        for r in range(nn,row-nn):
            for c in range(nn,col-nn):
                # Extract the image nxn mask
                ar = A[r-nn:r+nn+1, c-nn:c+nn+1]

                # flattening the 2D array to 1D
                arr = np.sort(np.array(ar).ravel())
                A_mf[r][c] = arr[len(arr)//2] 
    
#     A_cv2_mf = cv2.medianBlur(A, n)
    
#     plt.figure(), plt.imshow(A, cmap='gray')
#     plt.figure(), plt.imshow(A_mf, cmap='gray')
#     plt.figure(), plt.imshow(A_cv2_mf, cmap='gray')
    
    return A_mf
    
