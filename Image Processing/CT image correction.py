## Flat Field Correction (FFC) by BBoDDo_lab ##

%matplotlib notebook
import numpy as np
import cv2
import matplotlib.pyplot as plt
import numba as nb
import parmap
import multiprocessing as multi
import time
start = time.time()

# def pixel_cor(iter):
#    for n in iter:
#        print('n :',n)
#        for j in range(-1,2):
#            for k in range(-1,2):
#                if num_y[n]+j == -1 or num_x[n]+k == -1 or num_y[n]+j == 576 or num_x[n]+k == 576:
#                    ar[j+1][k+1] = 0
#                    ar2[j+1][k+1] = 0
#                else:
#                    ar[j+1][k+1] = w[num_y[n]+j][num_x[n]+k]
#                    ar2[j+1][k+1] = org_I[num_y[n]+j][num_x[n]+k]
#        ar[1][1] = 0
#        ar2[1][1] = 0
#        corrected_w[num_y[n]][num_x[n]] = np.sum(ar)/np.count_nonzero(ar)
#        corrected_org_I[num_y[n]][num_x[n]] = np.sum(ar2)/np.count_nonzero(ar2)



# def main(sens):

B = cv2.imread(r'D:\Remedi\Exercise\Xray\Offset.png', -1) # offset image


for i in range(2,3):
    print('i :', i)

    org_I = cv2.imread(r'D:\Remedi\Exercise\Xray\objects_median\object (' + str(i) + ').png', -1) # original image

    w = cv2.imread(r'D:\Remedi\Exercise\Xray\white_median\white (' + str(i) + ').png', -1) # white image

    ## 1.dead & bad pixel correction
    corrected_w = w.copy()
    corrected_org_I = org_I.copy()

    c = np.mean(corrected_w)
    p = np.abs(corrected_w - c)

    ## 2. line elimination
    # FFT
    F_w = np.fft.fft2(corrected_w)
    Fshift_w = np.fft.fftshift(F_w)
    F_cor = np.fft.fft2(corrected_org_I)
    Fshift_cor = np.fft.fftshift(F_cor)


    magnitude_spectrum = 20*np.log(np.abs(Fshift_w))
    magnitude_spectrum2 = 20*np.log(np.abs(Fshift_cor))
    
    Fshift_sub = np.subtract(Fshift_cor, Fshift_w)
    magnitude_spectrum3 = 20*np.log(np.abs(Fshift_sub))
    fshift_sub = np.fft.ifftshift(Fshift_sub)
    eximage = np.uint16(np.abs(np.fft.ifft2(fshift_sub))) 
#     plt.figure()
#     plt.imshow(magnitude_spectrum3, cmap='gray')
#     plt.figure()
#     plt.imshow(eximage, cmap='gray')    
    
#     plt.figure()
#     plt.imshow(magnitude_spectrum, cmap='gray')
#     plt.figure()
#     plt.imshow(magnitude_spectrum2, cmap='gray')

    # Eliminate frequency
    [row, col] = org_I.shape
    [row2, col2] = np.array([row, col], dtype=np.int) // 2
    row2_range = 1
    col2_range = 5
    Fshift_w[:row2-row2_range-1, col2-col2_range-1:col2+col2_range] = 0
    Fshift_w[row2+row2_range:, col2-col2_range-1:col2+col2_range] = 0
    Fshift_cor[:row2-row2_range-1, col2-col2_range-1:col2+col2_range] = 0
    Fshift_cor[row2+row2_range:, col2-col2_range-1:col2+col2_range] = 0
    Fshift_sub[:row2-row2_range-1, col2-col2_range-1:col2+col2_range] = 0
    Fshift_sub[row2+row2_range:, col2-col2_range-1:col2+col2_range] = 0    
#         Fshift[np.r_[:row2-row2_range-1,row2+row2_range:], col2-col2_range-1:col2+col2_range] = 0

    # IFFT
    fishift_w = np.fft.ifftshift(Fshift_w)
    corrected_w = np.uint16(np.abs(np.fft.ifft2(fishift_w)))
    fishift_cor = np.fft.ifftshift(Fshift_cor)
    corrected_org_I = np.uint16(np.abs(np.fft.ifft2(fishift_cor)))
    
#     fshift_sub = np.fft.ifftshift(Fshift_sub)
#     eximage = np.uint16(np.abs(np.fft.ifft2(fshift_sub))) 
#     plt.figure()
#     plt.imshow(magnitude_spectrum3, cmap='gray')
#     plt.figure()
#     plt.imshow(eximage, cmap='gray') 
    
    ## 3.flat field correction
    c = np.mean(corrected_w) # constant
    FFC = np.uint16(np.divide(c*( corrected_org_I-B), (corrected_w-B)))

    print("time :", time.time() - start)

#     plt.figure()
#         plt.subplot(241), plt.imshow(org_I, cmap='gray'), plt.title('Original Image')
#         plt.subplot(243), plt.imshow(corrected_org_I, cmap='gray'), plt.title('corrected original Image')
#         plt.subplot(244), plt.imshow(FFC, cmap='gray'), plt.title('FFC + FFT')
#         plt.subplot(245), plt.imshow(w, cmap='gray'), plt.title('w')
#         plt.subplot(247), plt.imshow(corrected_w, cmap='gray'), plt.title('corrected w')
#         plt.subplot(248), plt.imshow(B, cmap='gray'), plt.title('B')
    plt.figure()
    plt.imshow(corrected_w, cmap='gray')
    plt.figure()
    plt.imshow(FFC, cmap='gray')
    plt.show()

#     cv2.imwrite(r'D:\Remedi\Exercise\Xray\corrected images_median\FFC (' + str(i) + ').png', FFC)
#         cv2.imwrite(r'E:\Remedi\Exercise\Xray\objects\corrected_org_I (' + str(i) + ').png', corrected_org_I)
#         cv2.imwrite(r'E:\Remedi\Exercise\Xray\white\corrected_w (' + str(i) + ').png', corrected_w)

# num_cores = multi.cpu_count()
# pool = multi.Pool(processes=num_cores)
# pool.map(main, [0.99])
# pool.close()
# pool.join()

# num_cores = multi.cpu_count()
# pool = multi.Pool(num_cores)
# pool.apply_async(main, [0.99])
# pool.close()
# pool.join()

# num_cores = multi.cpu_count()
# parmap.map(main, [0.99], pm_processes=num_cores)

# main(1)

# print("time :", time.time() - start)

