from matplotlib.collections import LineCollection
import numpy as np
from collections import deque

class DecayLine(object):
    def __init__(self, n_points, tail_length, rgb_color, zorder=2):
        self.n_points = int(n_points)
        self.tail_length = int(tail_length)
        self.rgb_color = rgb_color
        self._zorder = zorder
        self.lc = None

    def __str__(self):
        if not hasattr(self, 'points') or not hasattr(self, 'segments'):
            return ""
        res = "DecayLine:"+"\n\t{}".format(self.segments)
        return res

    def set_data(self, x=None, y=None):
        if x is None or y is None:
            self.lc = LineCollection([], linewidths=1.0, zorder=self._zorder)
        else:
            # ensure we don't start with more points than we want
            x = x[-self.n_points:]
            y = y[-self.n_points:]
            # create a list of points with shape (len(x), 1, 2)
            # array([[[  x0  ,  y0  ]],
            #        [[  x1  ,  y1  ]],
            #        ...,
            #        [[  xn  ,  yn  ]]])
            #self.points = np.array([x, y]).T.reshape(-1, 1, 2)
            if not hasattr(self, 'points'):
                self.points = deque([[x[i], y[i]] for i in range(len(x))])
            else:
                for i in range(len(x)):
                    self.points.append([x[i], y[i]])
            # group each point with the one following it (shape (len(x)-1, 2, 2)):
            # array([[[  x0  ,   y0  ],
            #         [  x1  ,   y1  ]],
            #        [[  x1  ,   y1  ],
            #         [  x2  ,   y2  ]],
            #         ...
            # self.segments = np.concatenate([self.points[:-1], self.points[1:]],  axis=1)
            if len(self.points)>1:
                pts = np.array(self.points).reshape(-1, 1, 2)
                self.segments = np.concatenate([pts[:-1], pts[1:]], axis=1)
                if hasattr(self, 'alphas'):
                    del self.alphas
                if hasattr(self, 'rgba_colors'):
                    del self.rgba_colors

                if self.lc is None:
                    self.lc = LineCollection(self.segments, colors=self.get_colors(), linewidths=1.0, zorder=self._zorder)
                self.lc.set_segments(self.segments)
                self.lc.set_color(self.get_colors())
            else:
                if self.lc is None:
                    self.lc = LineCollection([], linewidths=1.0, zorder=self._zorder)

    def get_LineCollection(self):
        if not hasattr(self, 'lc'):
            self.set_data()
        return self.lc

    def get_label(self):
        """Return the label used for this artist in the legend."""
        if self.lc is None:
            return ""
        return self.lc.get_label()

    def set_label(self, s):
        if self.lc is not None:
            self.lc.set_label(s)

    def add_point(self, x, y):
        if not hasattr(self, 'points') or not hasattr(self, 'segments'):
            self.set_data([x],[y])
        else:
            # TODO: could use a circular buffer to reduce memory operations...
            # self.segments = np.concatenate((self.segments,[[self.points[-1][0],[x,y]]]))
            # self.points = np.concatenate((self.points, [[[x,y]]]))
            self.points.append([x, y])
            # remove points if necessary:
            while len(self.points) > self.n_points:
                self.points.popleft()
            pts = np.array(self.points).reshape(-1, 1, 2)
            self.segments = np.concatenate([pts[:-1], pts[1:]], axis=1)
            self.lc.set_segments(self.segments)
            self.lc.set_color(self.get_colors())

    @property
    def npoints(self):
        if not hasattr(self, 'points'):
            return 0
        else:
            #return self.points.shape[0]
            return len(self.points)

    def get_alphas(self):
        n_segments = self.n_points-1
        n = len(self.segments)
        # n = self.points.shape[0]
        if n < n_segments:
            rest_length = n_segments - self.tail_length
            if n <= rest_length:
                return np.ones(n)
            else:
                tail_length = n - rest_length
                tail = np.linspace(1./tail_length, 1., tail_length)
                rest = np.ones(rest_length)
                return np.concatenate((tail, rest), axis=None)
        else: # n == n_segments
            if not hasattr(self, 'alphas'):
                tail = np.linspace(1./self.tail_length, 1., self.tail_length)
                rest = np.ones(n_segments - self.tail_length)
                self.alphas = np.concatenate((tail, rest), axis=None)
            return self.alphas

    def get_colors(self):
        n_segments = self.n_points-1
        n = len(self.segments)
        if  n < 2:
            return [self.rgb_color+[1.] for i in range(n)]
        if n < n_segments:
            alphas = self.get_alphas()
            rgba_colors = np.zeros((n, 4))
            # first place the rgb color in the first three columns
            rgba_colors[:,0:3] = self.rgb_color
            # and the fourth column needs to be your alphas
            rgba_colors[:, 3] = alphas
            return rgba_colors
        else:
            if hasattr(self, 'rgba_colors'):
                pass
            else:
                alphas = self.get_alphas()
                rgba_colors = np.zeros((n, 4))
                # first place the rgb color in the first three columns
                rgba_colors[:,0:3] = self.rgb_color
                # and the fourth column needs to be your alphas
                rgba_colors[:, 3] = alphas
                self.rgba_colors = rgba_colors
            return self.rgba_colors