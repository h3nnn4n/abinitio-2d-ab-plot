# pylint: disable=E1101
import cairo

from math import pi


class Plotter:
    def __init__(self, data):
        self.data = data
        self.ball_radius = 5
        self.a_color = (1, 0, 0)
        self.b_color = (0, 0, 1)
        self.line_width = 1
        self.line_color = (0, 0, 0)

        self.set_canvas()

        self.scale_data()

    def scale_data(self):
        min_x = self.x_axis_range()[0]
        min_y = self.y_axis_range()[0]

        scale = self.biggest_range()

        new_data = []

        for x, y, k in self.data:
            x_ = (x - min_x) / scale
            y_ = (y - min_y) / scale

            new_data.append((x_, 1.0 - y_, k))

        self.data = new_data

    def set_canvas(self, width=600, height=600, scale=4):
        self.scale = scale
        self.width = width
        self.height = height

        self.create_surface()
        self.set_background()

        return self

    def create_surface(self):
        self.surface = cairo.ImageSurface(
            cairo.FORMAT_ARGB32,
            self.width * self.scale,
            self.height * self.scale
        )
        self.surface.set_device_scale(self.scale, self.scale)
        self.ctx = cairo.Context(self.surface)

        return self

    def set_background(self, r=1, g=1, b=1):
        if isinstance(r, tuple):
            r, g, b, _ = r
        self.ctx.set_source_rgb(r, g, b)
        self.ctx.rectangle(0, 0, self.width, self.height)
        self.ctx.fill()

        return self

    def save(self, name='output.png'):
        self.surface.write_to_png(name)

    def biggest_range(self):
        x_range = self.x_axis_range()
        y_range = self.y_axis_range()

        return max(x_range[1] - x_range[0], y_range[1] - y_range[0])

    def x_axis_range(self):
        lower = float('inf')
        upper = float('-inf')

        for x, _, _ in self.data:
            lower = min(lower, x)
            upper = max(upper, x)

        return lower, upper

    def y_axis_range(self):
        lower = float('inf')
        upper = float('-inf')

        for _, y, _ in self.data:
            lower = min(lower, y)
            upper = max(upper, y)

        return lower, upper

    def render(self):
        ctx = self.ctx
        scale = self.width * 0.9

        ctx.translate(
            self.width * 0.05,
            self.height * 0.05
        )

        self.set_color(self.line_color)
        ctx.set_line_width(self.line_width)

        for x, y, _ in self.data:
            ctx.line_to(x * scale, y * scale)

        ctx.stroke()

        for x, y, kind in self.data:
            if kind:
                self.set_color(self.a_color)
            else:
                self.set_color(self.b_color)

            ctx.arc(x * scale, y * scale, self.ball_radius, 0, 2 * pi)

            ctx.fill()

    def set_color(self, r=1, g=1, b=1):
        if isinstance(r, tuple):
            r, g, b = r

        self.ctx.set_source_rgb(r, g, b)
