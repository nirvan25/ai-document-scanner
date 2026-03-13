import numpy as np
from matplotlib.lines import Line2D
from matplotlib.artist import Artist


class PolygonInteractor(object):

    showverts = True
    epsilon = 5

    def __init__(self, ax, poly):

        if poly.figure is None:
            raise RuntimeError("Polygon must be added to figure first")

        self.ax = ax
        canvas = poly.figure.canvas
        self.poly = poly

        x, y = zip(*self.poly.xy)
        self.line = Line2D(x, y, marker="o", markerfacecolor="r", animated=True)

        self.ax.add_line(self.line)

        self._ind = None

        canvas.mpl_connect("button_press_event", self.button_press_callback)
        canvas.mpl_connect("button_release_event", self.button_release_callback)
        canvas.mpl_connect("motion_notify_event", self.motion_notify_callback)

        self.canvas = canvas

    def get_poly_points(self):
        return np.asarray(self.poly.xy)

    def get_ind_under_point(self, event):

        xy = np.asarray(self.poly.xy)

        xyt = self.poly.get_transform().transform(xy)

        xt, yt = xyt[:, 0], xyt[:, 1]

        d = np.sqrt((xt - event.x) ** 2 + (yt - event.y) ** 2)

        ind = np.argmin(d)

        if d[ind] >= self.epsilon:
            ind = None

        return ind

    def button_press_callback(self, event):

        if not self.showverts:
            return

        if event.inaxes is None:
            return

        if event.button != 1:
            return

        self._ind = self.get_ind_under_point(event)

    def button_release_callback(self, event):

        if event.button != 1:
            return

        self._ind = None

    def motion_notify_callback(self, event):

        if not self.showverts:
            return

        if self._ind is None:
            return

        if event.inaxes is None:
            return

        if event.button != 1:
            return

        x, y = event.xdata, event.ydata

        self.poly.xy[self._ind] = x, y

        if self._ind == 0:
            self.poly.xy[-1] = x, y

        elif self._ind == len(self.poly.xy) - 1:
            self.poly.xy[0] = x, y

        self.line.set_data(zip(*self.poly.xy))
        self.canvas.draw()