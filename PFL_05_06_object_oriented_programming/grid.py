import numpy as np
import matplotlib.pyplot as plt

class Grid(object):
    """Some Doc about grid objects

    """

    def __init__(self, lon, lat, time):
        self.lon = lon
        self.lat = lat
        self.time = time
        self.grid_type = "grid"

    def print_whoAmI(self):
        print("I am a %s" % self.grid_type)

    @staticmethod
    def grid(lon, lat, time):
        if len(lon.shape) == 1:
            return RectilinearGrid(lon, lat, time)
        else:
            return CurvilinearGrid(lon, lat, time)


class RectilinearGrid(Grid):
    def __init__(self, lon, lat, time):
        super(RectilinearGrid, self).__init__(lon, lat, time)
        self.grid_type = "rectilinear_grid"

        assert len(self.lon.shape) == 1
        assert len(self.lat.shape) == 1
        self.xdim = self.lon.size
        self.ydim = self.lat.size

    def plot(self):
        lon_mg, lat_mg = np.meshgrid(self.lon, self.lat)
        plt.plot(lon_mg, lat_mg, 'b')
        plt.plot(lon_mg.transpose(), lat_mg.transpose(), 'b')
        return plt

class CurvilinearGrid(Grid):
    def __init__(self, lon, lat, time):
        super(CurvilinearGrid, self).__init__(lon, lat, time)
        self.grid_type = "curvilinear_grid"

        assert len(self.lon.shape) == 2
        assert len(self.lat.shape) == 2
        self.xdim = self.lon.shape[0]
        self.ydim = self.lat.shape[1]

    def plot(self):
        plt.plot(self.lon, self.lat, 'b')
        plt.plot(self.lon.transpose(), self.lat.transpose(), 'b')
        return plt

    def print_whoAmI(self):
        print("I am a super fancy %s" % self.grid_type)
