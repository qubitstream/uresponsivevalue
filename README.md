# uresponsivevalue

## Description

**uresponsivevalue** is a library intended for [MicroPython](https://micropython.org/) for
smoothing out values such as those yielded by analog inputs, usually suffering
from a lot of jitter and therefore jumpy values. You can however use it for any sequence of values.

**Note**: Although it is intended for MicroPython, it is fully usable in "regular"
Python as well.

uresponsivevalue is heavily inspired by Damien Clarke's
[ResponsiveAnalogRead](https://github.com/dxinteractive/ResponsiveAnalogRead)
C++ library for Arduinos. If you want to know how it works, check out his
excellent [blog post](http://damienclarke.me/code/posts/writing-a-better-noise-reducing-analogread).

## Mini Documentation

```python
ResponsiveValue(value_func, sleep_enable=True, snap_multiplier=0.01, edge_snap_enable=True, max_value=1024, activity_threshold=4)
```
- `value_func`: a callable without any parameters - this reads the "new" value every time `update()` is called.
   Returned values should go from 0 to `max_value` (see below).

**Note**: If your callable expects parameters, pass in a lambda, e.g.:
`rv = ResponsiveValue(lambda: your_function(1,2,3))`

_optional:_

- `sleep_enable`: sleep minimizes the amount of value changes over time.
- `snap_multiplier`: controls the amount of easing; must be within 0 an 1.
- `edge_snap_enable`: ensures that values on the end of the spectrum can be easily reached.
- `max_value`: the maximum value `value_func` may receive. For the ESP8266's ADC, this is 1024.
- `activity_threshold`: minimum amount of change to register as movement.

While the defaults are sensible, feel free to experiment to get a satisfying result.

If you need more information on the parameters, check out their description
[here](https://github.com/dxinteractive/ResponsiveAnalogRead).

---

```python
ResponsiveValue.update(raw_value=None)
```

Updates and calculates the new value by calling `value_func`.

_optional:_

- `raw_value`: uses this value instead of one returned by `value_func`.

---

```python
ResponsiveValue.responsive_value
```

Holds the current actual "smoothed out" value.

---

```python
ResponsiveValue.has_changed
```

`True` if there's a new `responsive_value`, else `False`.

## Example

This example has been tested on a NodeMCU microcontroller with the MicroPython firmware.

```python
from machine import ADC
from uresponsivevalue import ResponsiveValue

analog_pin = ADC(0)
responsive_value = ResponsiveValue(analog_pin.read) # a callable is passed - note the missing parentheses

while True:
    responsive_value.update()
    print('{}\t{}\t{}\t{}\t{}'.format(
        responsive_value.has_changed,
        responsive_value.raw_value,
        responsive_value.responsive_value, # the smoothed out value
        responsive_value.sleeping,
        responsive_value._error_EMA))
```

## License

    The MIT License

    Copyright (c) 2016 Christoph Haunschmidt

    Permission is hereby granted, free of charge,
    to any person obtaining a copy of this software and
    associated documentation files (the "Software"), to
    deal in the Software without restriction, including
    without limitation the rights to use, copy, modify,
    merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom
    the Software is furnished to do so,
    subject to the following conditions:

    The above copyright notice and this permission notice
    shall be included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
    OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR
    ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
    TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
    SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
