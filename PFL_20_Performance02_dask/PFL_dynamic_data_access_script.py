import numpy as np
import xarray as xr
from dask import array as da_array
import psutil
from os import getpid
from os import path
import gc
from time import time as ostime
from time import sleep
# from matplotlib.pyplot import imshow
import matplotlib.pyplot as plt
from threading import Thread
from threading import Event
# from scipy import misc
from PIL import Image
import math

class BackgroundMeasureMemory(object):
    def __init__(self, interval, process=None):
        self.interval = interval
        self.start = ostime()
        self._mem_start = psutil.Process(getpid()).memory_info().rss
        self._mem_measurement = []
        if self._mem_start > 0:
            self._mem_measurement.append(0)
        self.event = Event()
        self.thread = Thread(target=self._target)
        self.thread.start()

    def __del__(self):
        del self._mem_measurement

    def _target(self):
        if self._mem_start <= 0:
            self._mem_start = psutil.Process(getpid()).memory_info().rss
            self._mem_measurement.append(0)
        while not self.event.is_set():
            self._mem_measurement.append( (psutil.Process(getpid()).memory_info().rss-self._mem_start)/1024.0 )
            sleep(self.interval)

    def stop(self):
        self.event.set()
        self.thread.join()

    def get_measurement(self):
        return self._mem_measurement


def get_lib(a):
    return np if not isinstance(a, da_array.core.Array) else da_array

def convolve(a, kernel, with_gc=False):
    out_buffer = np.zeros(a.shape, dtype=a.dtype)
    assert a.dtype==kernel.dtype
    ik_buffer = np.zeros(kernel.shape, dtype=a.dtype)
    out_mat = np.zeros(kernel.shape, dtype=a.dtype, order='C')
    k_xi_diff = int((kernel.shape[0]-1)/2)
    k_yi_diff = int((kernel.shape[1]-1)/2)
    # print("A shape: {}, K shape: {}, K_diff: {}".format(a.shape, kernel.shape, (k_xi_diff, k_yi_diff)))
    N = a.shape[0]*a.shape[1]
    print("N = {}".format(N))
    last_out = -1
    use_da = isinstance(a, da_array.core.Array)
    for i in range(a.shape[0] * a.shape[1]):
        ik_buffer.fill(0)
        xi = int(i / a.shape[0])
        yi = int(i % a.shape[0])
        xi_a_min = max((xi - k_xi_diff), 0)
        yi_a_min = max((yi - k_yi_diff), 0)  # %a.shape[0]
        xi_a_max = min((xi + k_xi_diff), a.shape[0] - 1)
        yi_a_max = min((yi + k_yi_diff), a.shape[1] - 1)
        k_xi_a_min = (xi_a_min - xi) + k_xi_diff
        k_yi_a_min = (yi_a_min - yi) + k_yi_diff
        k_xi_a_max = (xi_a_max - xi) + k_xi_diff
        k_yi_a_max = (yi_a_max - yi) + k_yi_diff
        ik_buffer[k_xi_a_min:(k_xi_a_max + 1), k_yi_a_min:(k_yi_a_max + 1)] = a[xi_a_min:(xi_a_max + 1),
                                                                              yi_a_min:(yi_a_max + 1)]

        # for k_i in range(kernel.shape[0]*kernel.shape[1]):
        #     k_xi = int(k_i / kernel.shape[0])
        #     k_yi = int(k_i % kernel.shape[0])
        #     xi_a_min = np.max((xi-k_xi_diff+k_xi), 0)
        #     yi_a_min = np.max((yi-k_yi_diff+k_yi), 0) # %a.shape[0]
        #     xi_a_max = np.min((xi-k_xi_diff+k_xi), a.shape[0])
        #     yi_a_max = np.min((yi-k_yi_diff+k_yi), a.shape[1])
        #     if use_da:
        #         ik_buffer[k_xi, k_yi] = a[xi_a_min, yi_a_min]
        #     else:
        #         ik_buffer[k_xi, k_yi] = a[xi_a_min, yi_a_min]
        perc_int = int((float(i)/N)*100.0)
        if (perc_int % 10) == 0 and perc_int != last_out:
            print("Convolution done by {} percent ...".format(perc_int))
            last_out = perc_int
            if with_gc:
                gc.collect()
        np.dot(ik_buffer, kernel, out_mat)
        out_buffer[xi, yi] = np.nanmean(out_mat.flatten())
    # for xi in range(a.shape[0]):
    #     for yi in range(a.shape[1]):
            # for k_xi in range(kernel.shape[0]):
            #     for k_yi in range(kernel.shape[1]):
            #         xi_a = (xi-k_xi_diff+k_xi)%a.shape[0]
            #         yi_a = (yi-k_yi_diff+k_yi)%a.shape[1]
            #         if isinstance(a, da_array.core.Array):
            #             ik_buffer[k_xi, k_yi] = a[xi_a, yi_a].compute()
            #         else:
            #             ik_buffer[k_xi, k_yi] = a[xi_a, yi_a]
            # out_mat = np.dot(ik_buffer, kernel)
            # out_buffer[xi, yi] = np.nanmean(out_mat)
    return out_buffer


def conv_arr_img(data):
    return (255.0 / data.max() * (data - data.min())).astype(np.uint8)


x, y = np.meshgrid(np.linspace(-1,1,5), np.linspace(-1,1,5))
d = np.sqrt(x*x+y*y)
sigma, mu = 1.0, 0.0
g = np.exp(-( (d-mu)**2 / ( 2.0 * sigma**2 ) ) ).astype(dtype=np.float32)


if __name__ == '__main__':
    timer_overall = BackgroundMeasureMemory(0.01)

    # ==== ADD SIMPLE IN-MEMORY EXAMPLE HERE BEFORE GOING TO FILES ==== #
    timed_mem_collection_1 = BackgroundMeasureMemory(0.01)
    sleep(0.1)
    time_s_genStommel_np = ostime()
    a = 10000 * 1e3
    b = 10000 * 1e3
    scalefac = 0.05
    lon = np.linspace(0, a, 200, dtype=np.float32)
    lat = np.linspace(0, b, 200, dtype=np.float32)
    U = np.zeros((lon.size, lat.size), dtype=np.float32)
    V = np.zeros((lon.size, lat.size), dtype=np.float32)
    beta = 2e-11
    r = 1 / (11.6 * 86400)
    es = r / (beta * a)
    for i in range(lon.size):
        for j in range(lat.size):
            xi = lon[i] / a
            yi = lat[j] / b
            U[i, j] = -(1 - math.exp(-xi/es) - xi) * math.pi**2 * np.cos(math.pi*yi)*scalefac
            V[i, j] = (math.exp(-xi/es)/es - 1) * math.pi * np.sin(math.pi*yi)*scalefac
    del lon
    del lat
    U_img = Image.fromarray(conv_arr_img(U))
    U_img.save(path.join("./", "U.png"))
    del U_img; U_img = None
    V_img = Image.fromarray(conv_arr_img(V))
    V_img.save(path.join("./", "V.png"))
    del V_img; V_img = None
    stommel_u_np_base = np.array(U)
    stommel_v_np_base = np.array(V)
    time_e_genStommel_np = ostime()
    print("Time to generate stommel dataset in NumPy: {} sec.".format(time_e_genStommel_np - time_s_genStommel_np))
    time_s_conv_np = ostime()
    d_res_np = convolve(stommel_u_np_base, g)
    time_e_conv_np = ostime()
    print("Time to convolve stommel dataset with 5x5 gaussian kernel in NumPy: {} sec.".format(
        time_e_conv_np - time_s_conv_np))
    # imshow(np.asarray(np.array(d_res_np)))
    img_1_1 = Image.fromarray(conv_arr_img(d_res_np))
    img_1_1.save(path.join("./", "convolve_np.png"))
    del img_1_1; img_1_1 = None
    del d_res_np; d_res_np = None
    time_s_gradmag_np = ostime()
    # d_res_np = np.square(stommel_u_np_base*stommel_v_np_base)/(np.fabs(stommel_u_np_base) * np.fabs(stommel_v_np_base))
    d_mag_np = np.sqrt(np.square(stommel_u_np_base) + np.square(stommel_v_np_base))
    time_e_gradmag_np = ostime()
    print("Time to stommel gradient magnitude in NumPy: {} sec.".format(time_e_gradmag_np-time_s_gradmag_np))
    # imshow(np.asarray(np.array(d_res_np)))
    img_1_2 = Image.fromarray(conv_arr_img(d_mag_np))
    img_1_2.save(path.join("./", "flowmag_np.png"))
    del img_1_2; img_1_2 = None
    del d_mag_np; d_mag_np = None
    del stommel_u_np_base; stommel_u_np_base = None
    del stommel_v_np_base; stommel_v_np_base = None
    sleep(0.1)
    timed_mem_collection_1.stop()

    fig, ax = plt.subplots(1, 1, figsize=(15, 9))
    plot_mem = timed_mem_collection_1.get_measurement()
    plot_t = np.arange(0, len(plot_mem), dtype=np.float32) * 0.01
    # ax.plot(x, plot_t, 'o-', label="time_spent [sec]")
    # ax.plot(x, plot_mem, 'x-', label="memory_used [100 MB]")
    ax.plot(plot_t, plot_mem)
    ax.set_ylim([0, 2400])
    ax.legend()
    # ax.set_xlabel('iteration')
    ax.set_xlabel('time_spent [sec]')
    ax.set_ylabel('memory_used [KB]')
    plt.savefig(path.join("./", "mem_conv_np_base.png"), dpi=300, format='png')
    del timed_mem_collection_1
    del plot_mem
    del plot_t
    del ax
    del fig

    # ==== construct a dynamic access array from numpy ==== #
    timed_mem_collection_2 = BackgroundMeasureMemory(0.005)
    sleep(0.1)
    time_s_convertStommel_da = ostime()
    stommel_u_da_base = da_array.from_array(U, chunks=(64, 64))
    stommel_v_da_base = da_array.from_array(V, chunks=(64, 64))
    time_e_convertStommel_da = ostime()
    print(
        "Time to generate stommel dataset in Dask: {} sec.".format(time_e_convertStommel_da - time_s_convertStommel_da))
    time_s_conv_da = ostime()
    d_res_da = convolve(stommel_u_da_base, g)
    # d_res_da = da_array.from_array(d_res_np, chunks=(64, 64))
    time_e_conv_da = ostime()
    print("Time to convolve stommel dataset with 5x5 gaussian kernel in Dask: {} sec.".format(
        time_e_conv_da - time_s_conv_da))
    # imshow(np.asarray(np.array(d_res_np)))
    img_2_1 = Image.fromarray(conv_arr_img(np.array(d_res_da)))
    img_2_1.save(path.join("./", "convolve_da.png"))
    del img_2_1; img_2_1 = None
    del d_res_da; d_res_da = None
    time_s_gradmag_da = ostime()
    # d_res_da = da_array.square(stommel_u_da_base*stommel_v_da_base)/(da_array.fabs(stommel_u_da_base) * np.fabs(stommel_v_da_base))
    d_mag_da = da_array.sqrt(da_array.square(stommel_u_da_base) + da_array.square(stommel_v_da_base))
    time_e_gradmag_da = ostime()
    print("Time to stommel gradient magnitude in NumPy: {} sec.".format(time_e_gradmag_da-time_s_gradmag_da))
    # imshow(np.asarray(np.array(d_res_da)))
    img_2_2 = Image.fromarray(conv_arr_img(np.array(d_mag_da)))
    img_2_2.save(path.join("./", "flowmag_da.png"))
    del img_2_2; img_2_2 = None
    del d_mag_da; d_mag_da = None
    del stommel_u_da_base; stommel_u_da_base = None
    del stommel_v_da_base; stommel_v_da_base = None
    # del U; U = None
    # del V; V = None
    sleep(0.1)
    timed_mem_collection_2.stop()

    fig_da, ax_da = plt.subplots(1, 1, figsize=(15, 9))
    plot_mem = timed_mem_collection_2.get_measurement()
    plot_t = np.arange(0, len(plot_mem), dtype=np.float32) * 0.005
    # ax.plot(x, plot_t, 'o-', label="time_spent [sec]")
    # ax.plot(x, plot_mem, 'x-', label="memory_used [100 MB]")
    ax_da.plot(plot_t, plot_mem)
    ax_da.set_ylim([0, 2400])
    ax_da.legend()
    # ax.set_xlabel('iteration')
    ax_da.set_xlabel('time_spent [sec]')
    ax_da.set_ylabel('memory_used [KB]')
    plt.savefig(path.join("./", "mem_conv_da_base.png"), dpi=300, format='png')
    del timed_mem_collection_2
    del plot_mem
    del plot_t
    del ax_da
    del fig_da

    # ==== construct a dynamic access array from numpy ==== #
    timed_mem_collection_3 = BackgroundMeasureMemory(0.005)
    sleep(0.1)
    time_s_convertStommel_da = ostime()
    stommel_u_da_base = da_array.from_array(U, chunks=(64, 64))
    stommel_v_da_base = da_array.from_array(V, chunks=(64, 64))
    time_e_convertStommel_da = ostime()
    print(
        "Time to generate stommel dataset in Dask: {} sec.".format(time_e_convertStommel_da - time_s_convertStommel_da))
    time_s_conv_da = ostime()
    d_res_da = convolve(stommel_u_da_base, g, with_gc=True)
    # d_res_da = da_array.from_array(d_res_np, chunks=(64, 64))
    time_e_conv_da = ostime()
    print("Time to convolve stommel dataset with 5x5 gaussian kernel in Dask (with GC): {} sec.".format(
        time_e_conv_da - time_s_conv_da))
    del stommel_u_da_base; stommel_u_da_base = None
    del stommel_v_da_base; stommel_v_da_base = None
    del U; U = None
    del V; V = None
    sleep(0.1)
    timed_mem_collection_3.stop()

    fig_da, ax_da = plt.subplots(1, 1, figsize=(15, 9))
    plot_mem = timed_mem_collection_3.get_measurement()
    plot_t = np.arange(0, len(plot_mem), dtype=np.float32) * 0.005
    # ax.plot(x, plot_t, 'o-', label="time_spent [sec]")
    # ax.plot(x, plot_mem, 'x-', label="memory_used [100 MB]")
    ax_da.plot(plot_t, plot_mem)
    ax_da.set_ylim([0, 2400])
    ax_da.legend()
    # ax.set_xlabel('iteration')
    ax_da.set_xlabel('time_spent [sec]')
    ax_da.set_ylabel('memory_used [KB]')
    plt.savefig(path.join("./", "mem_conv_da_base_wGC.png"), dpi=300, format='png')
    del timed_mem_collection_3
    del plot_mem
    del plot_t
    del ax_da
    del fig_da



    print("==== Example - file access - xarray - without dynamic loading (dask) ====")

    proc = psutil.Process(getpid())
    gc.collect()
    mem_used_before = proc.memory_info().rss
    stommel_data = xr.open_dataset("./stommelU.nc", decode_cf=True, engine='netcdf4')
    stommel_data['decoded'] = True
    xdim = stommel_data.dims['x']
    ydim = stommel_data.dims['y']
    print("xdim: {}; ydim: {}".format(xdim, ydim))
    stommel_u = stommel_data["vozocrtx"]
    if isinstance(stommel_u, xr.DataArray):
        stommel_u = stommel_u.data
    print("Matrix/DenseArray type: {}".format(type(stommel_u)))
    mem_used_after = proc.memory_info().rss
    print("Stommel dataset - memory size: {} KB".format((mem_used_after - mem_used_before) / 1024))
    coords_1 = np.random.randint((0, 0), (xdim, ydim), 2, dtype=np.int32)
    time_idx = 0
    depth_idx = 0
    print("Accessing element ({}, {}, {}, {})".format(time_idx, depth_idx, coords_1[1], coords_1[0]))
    d_element = stommel_u[time_idx, depth_idx, coords_1[1], coords_1[0]]
    print("Element value: {}".format(d_element))
    mem_used_after = proc.memory_info().rss
    print("Memory consumption: {} KB".format((mem_used_after - mem_used_before) / 1024))
    del d_element
    coords_2 = np.random.randint((0, 0), (xdim, ydim), 2, dtype=np.int32)
    coords = np.concatenate((coords_1.reshape(coords_1.shape[0], 1), coords_2.reshape(coords_2.shape[0], 1)), axis=1)
    slice_coords = [[np.min(coords, 0)[0], np.max(coords, 0)[0]],
                    [np.min(coords, 0)[1], np.max(coords, 0)[1]]]
    print(
        "Accessing subfield ({}, {}, {}:{}, {}:{})".format(time_idx, depth_idx, slice_coords[0][0], slice_coords[0][1],
                                                           slice_coords[1][0], slice_coords[1][1]))
    d_slice_1 = stommel_u[time_idx, depth_idx, slice_coords[0][0]:slice_coords[0][1],
                slice_coords[1][0]:slice_coords[1][1]]
    print("Sub-field 1: {}".format(d_slice_1))
    d_res = d_slice_1 * 5.0
    print("field 1 * 5: {}".format(d_res))
    mem_used_after = proc.memory_info().rss
    print("Memory consumption: {} KB".format((mem_used_after - mem_used_before) / 1024))
    del d_slice_1
    del d_res
    del stommel_u
    stommel_data.close()
    del stommel_data

    print("")
    print("")
    print("==== Example - file access - xarray - with dynamic loading (dask) ====")
    proc = psutil.Process(getpid())
    gc.collect()
    mem_used_before = proc.memory_info().rss
    stommel_data_da = xr.open_dataset("./stommelU.nc", decode_cf=True, engine='netcdf4', chunks={'x': 128, 'y': 128})
    stommel_data_da['decoded'] = True
    stommel_u_da = stommel_data_da["vozocrtx"]
    if isinstance(stommel_u_da, xr.DataArray):
        stommel_u_da = stommel_u_da.data
    print("Matrix/DenseArray type: {}".format(type(stommel_u_da)))
    mem_used_after = proc.memory_info().rss
    print("Stommel dataset - memory size: {} KB".format((mem_used_after-mem_used_before)/1024))
    print("Accessing element ({}, {}, {}, {})".format(time_idx, depth_idx, coords_1[1], coords_1[0]))
    d_element_da = stommel_u_da[time_idx, depth_idx, coords_1[1], coords_1[0]]
    print("Element value: {}".format(d_element_da.compute()))
    mem_used_after = proc.memory_info().rss
    print("Memory consumption: {} KB".format((mem_used_after-mem_used_before)/1024))
    del d_element_da
    print("Accessing subfield ({}, {}, {}:{}, {}:{})".format(time_idx, depth_idx, slice_coords[0][0],slice_coords[0][1], slice_coords[1][0],slice_coords[1][1]))
    d_slice_1_da = stommel_u_da[time_idx, depth_idx, slice_coords[0][0]:slice_coords[0][1], slice_coords[1][0]:slice_coords[1][1]]
    print("Sub-field 1: {}".format(d_slice_1_da.compute()))
    d_res = d_slice_1_da * 5.0
    print("field 1 * 5: {}".format(d_res.compute()))
    mem_used_after = proc.memory_info().rss
    print("Memory consumption: {} KB".format((mem_used_after-mem_used_before)/1024))
    del d_slice_1_da
    del d_res
    del stommel_u_da
    stommel_data_da.close()
    del stommel_data_da

    timer_overall.stop()
    fig_da, ax_da = plt.subplots(1, 1, figsize=(30, 18))
    plot_mem = timer_overall.get_measurement()
    plot_t = np.arange(0, len(plot_mem), dtype=np.float32) * 0.01
    # ax.plot(x, plot_t, 'o-', label="time_spent [sec]")
    # ax.plot(x, plot_mem, 'x-', label="memory_used [100 MB]")
    ax_da.plot(plot_t, plot_mem)
    # ax_da.set_ylim([0, 2400])
    ax_da.legend()
    # ax.set_xlabel('iteration')
    ax_da.set_xlabel('time_spent [sec]')
    ax_da.set_ylabel('memory_used [KB]')
    plt.savefig(path.join("./", "mem_overall.png"), dpi=400, format='png')
    del timer_overall
    del plot_mem
    del plot_t