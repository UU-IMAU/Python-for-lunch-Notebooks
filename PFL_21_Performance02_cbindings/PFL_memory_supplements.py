import numpy
import math
from scipy.io import netcdf
from scipy.interpolate import interpn
from time import process_time as compute_ptimer_hr
from datetime import time, timedelta

def create_stommel_array():
    a = 10000 * 1e3
    b = 10000 * 1e3
    scalefac = 0.05
    lon = numpy.linspace(0, a, 100, dtype=numpy.float32)
    lat = numpy.linspace(0, b, 100, dtype=numpy.float32)
    U = numpy.zeros((lon.size, lat.size), dtype=numpy.float32)
    V = numpy.zeros((lon.size, lat.size), dtype=numpy.float32)
    beta = 2e-11
    r = 1 / (11.6 * 86400)
    es = r / (beta * a)
    for i in range(lon.size):
        for j in range(lat.size):
            xi = lon[i] / a
            yi = lat[j] / b
            U[i, j] = -(1 - numpy.exp(-xi / es) - xi) * numpy.pi ** 2 * numpy.cos(numpy.pi * yi) * scalefac
            V[i, j] = (numpy.exp(-xi / es) / es - 1) * numpy.pi * numpy.sin(numpy.pi * yi) * scalefac
    del lon
    del lat
    return U, V


class Particle():

    def __init__(self, x, y, keep_trace_history=False, dtype=numpy.float32):
        self._pt = numpy.array([x, y, .0], dtype=dtype)
        self._trace_history = None
        if keep_trace_history:
            self._trace_history = []

    def __del__(self):
        del self._pt
        if self._trace_history is not None:
            del self._trace_history[:]

    def advect(self, u_array, v_array, griddims, dt, fdt):
        if self._trace_history is not None and len(self._trace_history) < 1:
            self._trace_history.append(numpy.array(self._pt))
        lon_range = griddims[2][-1] - griddims[2][0]
        lat_range = griddims[1][-1] - griddims[1][0]
        pt = numpy.transpose(self._pt, (2, 1, 0))
        uv = numpy.array([interpn(griddims, u_array, pt, method='linear', fill_value=.0),
                          interpn(griddims, v_array, pt, method='linear', fill_value=.0)])
        self._pt[0:1] += ((uv * dt) / 1000.0)  # particles live on a km grid
        while self._pt[0] > griddims[2][-1]:
            self._pt[0] -= lon_range
        while self._pt[0] < griddims[2][0]:
            self._pt[0] += lon_range

        while self._pt[1] > griddims[1][-1]:
            self._pt[1] -= lat_range
        while self._pt[1] < griddims[1][0]:
            self._pt[1] += lat_range
        self._pt[2] += dt
        if self._trace_history is not None:
            self._trace_history.append(numpy.array(self._pt))

    def advect_uv(self, u, v, griddims, dt, fdt):
        if self._trace_history is not None and len(self._trace_history) < 1:
            self._trace_history.append(numpy.array(self._pt))
        self._pt[0] = self._pt[0] + ((u * dt) / 1000.0)  # particles live on a km grid
        self._pt[1] = self._pt[1] + ((v * dt) / 1000.0)  # particles live on a km grid
        # -- boundary condition treatment -- #
        if self._pt[0] > griddims[2][-1]:
            self._pt[0] = griddims[2][-1]
        if self._pt[0] < griddims[2][0]:
            self._pt[0] = griddims[2][0]

        if self._pt[1] > griddims[1][-1]:
            self._pt[1] = griddims[1][-1]
        if self._pt[1] < griddims[1][0]:
            self._pt[1] = griddims[1][0]

        self._pt[2] += dt
        # -- history tracing - only applicable for plotting the particle trajectories -- #
        if self._trace_history is not None:
            self._trace_history.append(numpy.array([self._pt[0], self._pt[1]]))

    @property
    def pt(self):
        return self._pt

    def point(self, tstep):
        if self._trace_history is not None:
            return self._trace_history[tstep]
        return self._pt

    def time_index(self, ft):
        # expect ft to be forward-linear
        f_dt = ft[1] - ft[0]
        f_interp = self._pt[2] / f_dt
        ti = int(math.floor(f_interp))
        return ti

    def time_partion(self, ft):
        # expect ft to be forward-linear
        f_dt = ft[1] - ft[0]
        f_interp = self._pt[2] / f_dt
        f_t = f_interp - math.floor(f_interp)
        return f_t


class Simulation():
    def __init__(self, fx, fy, ft, fu, fv, num_visual_traces=0, dtype=numpy.float32):
        self._dtype = dtype
        self._data = []
        self._fx = fx
        self._fy = fy
        self._ft = ft
        self._fu = fu
        self._fv = fv
        self._gdims = (self._ft, self._fy, self._fx)
        self._simtime = self._dtype(.0)
        self._num_visual_traces = num_visual_traces

    def __del__(self):
        del self._data[:]

    def __getitem__(self, item):
        max_item = len(self._data) - 1
        return self._data[min(item, max_item)]

    def __len__(self):
        return len(self._data)

    @property
    def sim_time(self):
        return self._simtime

    @property
    def sim_end_time(self):
        if type(self._ft[-1]) is numpy.timedelta64:
            return self._ft[-1].item().total_seconds()
        elif type(self._ft[-1]) not in [numpy.float64, numpy.float32]:
            return timedelta(self._ft[-1]).total_seconds()
        return self._ft[-1]

    @property
    def particles(self):
        result = numpy.array([p.pt for p in self._data])
        return result

    @particles.setter
    def particles(self, np_array):
        for i in range(0, np_array.shape[0]):
            self._data[i][:] = np_array[i, :]

    def add_particle(self, x, y):
        keep_trace_history = False
        if len(self._data) < self._num_visual_traces:
            keep_trace_history = True
        self._data.append(Particle(x, y, keep_trace_history))

    def advect_once(self, dt):
        fdt = self._ft[1] - self._ft[0]
        if type(fdt) not in [numpy.float64, numpy.float32]:
            fdt = timedelta(fdt).total_seconds()
        x = []
        y = []
        t = []
        for p in self._data:
            x.append(p.pt[0])
            y.append(p.pt[1])
            t.append(p.pt[2])
        pts = (numpy.array(t), numpy.array(y), numpy.array(x))
        us = interpn(self._gdims, self._fu, pts, method='linear', fill_value=.0)
        vs = interpn(self._gdims, self._fv, pts, method='linear', fill_value=.0)
        for i, p in enumerate(self._data):
            # p.advect(self._fu, self._fv, self._gdims, dt, fdt)
            p.advect_uv(us[i], vs[i], self._gdims, dt, fdt)
        self._simtime += dt

    def time_index(self):
        if len(self._data) < 1:
            return 0
        return self._data[0].time_index(self._ft)

    def time_partion(self):
        if len(self._data) < 1:
            return 0
        return self._data[0].time_partion(self._ft)

    def time_index_value(self, tx):
        # expect ft to be forward-linear
        f_dt = self._ft[1] - self._ft[0]
        if type(f_dt) is not numpy.float64:
            fdt = timedelta(f_dt).total_seconds()
        f_interp = tx / f_dt
        ti = int(math.floor(f_interp))
        return ti

    def time_partion_value(self, tx):
        # expect ft to be forward-linear
        f_dt = self._ft[1] - self._ft[0]
        if type(f_dt) is not numpy.float64:
            f_dt = timedelta(f_dt).total_seconds()
        f_interp = tx / f_dt
        f_t = f_interp - math.floor(f_interp)
        return f_t


class Simulation_Benchmark(Simulation):
    def __init__(self, fx, fy, ft, fu, fv, num_visual_traces=0, dtype=numpy.float32):
        super(Simulation_Benchmark, self).__init__(fx, fy, ft, fu, fv, num_visual_traces, dtype)
        self._io_mem_time = 0
        self._compute_time = 0

    def __del__(self):
        super(Simulation_Benchmark, self).__del__()

    def add_particle(self, x, y):
        stime = compute_ptimer_hr()
        super(Simulation_Benchmark, self).add_particle(x, y)
        etime = compute_ptimer_hr()
        self._io_mem_time += (etime - stime)

    def advect_once(self, dt):
        stime_calc = compute_ptimer_hr()
        fdt = self._ft[1] - self._ft[0]
        if type(fdt) not in [numpy.float64, numpy.float32]:
            fdt = timedelta(fdt).total_seconds()
        etime_calc = compute_ptimer_hr()
        self._compute_time += (etime_calc - stime_calc)
        x = []
        y = []
        t = []
        stime_mem = compute_ptimer_hr()
        for p in self._data:
            x.append(p.pt[0])
            y.append(p.pt[1])
            t.append(p.pt[2])
        pts = (numpy.array(t), numpy.array(y), numpy.array(x))
        etime_mem = compute_ptimer_hr()
        self._io_mem_time += (etime_mem - stime_mem)
        stime_calc = compute_ptimer_hr()
        us = interpn(self._gdims, self._fu, pts, method='linear', fill_value=.0)
        vs = interpn(self._gdims, self._fv, pts, method='linear', fill_value=.0)
        for i, p in enumerate(self._data):
            # p.advect(self._fu, self._fv, self._gdims, dt, fdt)
            p.advect_uv(us[i], vs[i], self._gdims, dt, fdt)
        self._simtime += dt
        etime_calc = compute_ptimer_hr()
        self._compute_time += (etime_calc - stime_calc)

    @property
    def io_mem_time(self):
        return self._io_mem_time

    @property
    def compute_time(self):
        return self._compute_time
