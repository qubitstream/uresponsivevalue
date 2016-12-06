# Smoothes out jittery readings
# Inspired by https://github.com/dxinteractive/ResponsiveAnalogRead


class ResponsiveValue:
    def __init__(
            self,
            value_func,
            sleep_enable=True,
            snap_multiplier=0.01,
            edge_snap_enable=True,
            max_value=1024,
            activity_threshold=4):
        self.value_func = value_func
        self.sleep_enable = sleep_enable
        self.snap_multiplier = snap_multiplier
        self.edge_snap_enable = edge_snap_enable
        self._max_value = max_value
        self.activity_threshold = activity_threshold
        self.raw_value = 0
        self.responsive_value = 0
        self.sleeping = False
        self.has_changed = True
        self._previous_responsive_value = 0
        self._smooth_value = 0
        self._error_EMA = 0

    def update(self, raw_value=None):
        self.raw_value = self.value_func() if raw_value is None else raw_value
        self._previous_responsive_value = self.responsive_value
        self.responsive_value = self._get_responsive_value(self.raw_value)
        self.has_changed = self.responsive_value != self._previous_responsive_value

    def _get_responsive_value(self, new_value):
        if self.sleep_enable and self.edge_snap_enable:
            if new_value < self.activity_threshold:
                new_value = new_value * 2 - self.activity_threshold
            elif new_value > self._max_value - self.activity_threshold:
                new_value = new_value * 2 - self._max_value + self.activity_threshold

        diff = abs(new_value - self._smooth_value)
        self._error_EMA += ((new_value - self._smooth_value) - self._error_EMA) * 0.4

        if self.sleep_enable:
            self.sleeping = abs(self._error_EMA) < self.activity_threshold
            if self.sleeping:
                return int(self._smooth_value)

        snap = self._snap_curve(diff * self.snap_multiplier)
        self._smooth_value += (new_value - self._smooth_value) * snap

        if self._smooth_value < 0:
            self._smooth_value = 0
        elif self._smooth_value > self._max_value:
            self._smooth_value = self._max_value

        return int(self._smooth_value)

    def _snap_curve(self, x):
        y = (1 - (1 / (x + 1))) * 2
        return 1 if y > 1 else y
