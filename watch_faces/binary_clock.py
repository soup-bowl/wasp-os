# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright (C) 2020 soup-bowl

"""Binary clock
~~~~~~~~~~~~~~~~~~

Displays the time using a binary-format display.
"""

import wasp
import watch
import fonts

COLORS = [0xE71C,0x738E]

class BinaryClockApp():
    NAME = 'Binary'

    def foreground(self):
        wasp.system.bar.clock = False
        self._draw(True)
        wasp.system.request_tick(1000)

    def sleep(self):
        return True

    def wake(self):
        self._draw()

    def tick(self, ticks):
        self._draw()

    def preview(self):
        wasp.system.bar.clock = False
        self._draw(True)
    
    def _pad_number(self, s, width):
        if len(s) >= width:
            return s
        else:
            return '0' * (width - len(s)) + s

    def _calculate_binary_dots(self, value, num_dots):
        # Convert value to 12-hour format if needed
        if num_dots == 4 and value > 12:
            value -= 12

        # Convert value to binary representation
        binary_value = bin(value % (2**num_dots))[2:]
        binary_value = '0' * (num_dots - len(binary_value)) + binary_value

        # Create an array to represent the dots, initialized with False
        dots = [False] * num_dots

        # Convert the binary representation to a list of True/False values
        for i in range(num_dots):
            if binary_value[i] == '1':
                dots[i] = True

        dots[:] = dots[::-1]
        return dots
    
    def _draw_indicator_spot(self, draw, pos_x, pos_y, active):
        if active:
            draw.fill(COLORS[0], pos_x, pos_y, 25, 25)
        else:
            draw.fill(COLORS[1], pos_x, pos_y, 25, 25)
    
    def _draw_clock(self, draw, time, pos_x, pos_y):
        real_pos_x = 240 - pos_x
        time_hour = self._calculate_binary_dots(time[3], 4)
        time_min = self._calculate_binary_dots(time[4], 6)

        adjusting_pos = real_pos_x
        for dot in time_hour:
            self._draw_indicator_spot(draw, adjusting_pos, pos_y, dot)
            adjusting_pos = adjusting_pos - 30
        
        adjusting_pos = (real_pos_x + 30)
        for dot in time_min:
            self._draw_indicator_spot(draw, adjusting_pos, (pos_y + 30), dot)
            adjusting_pos = adjusting_pos - 30

    def _day_string(self, now):
        return '{}-{}-{}'.format(now[0], self._pad_number(str(now[1]), 2), self._pad_number(str(now[2]), 2))

    def _draw(self, redraw=False):
        draw = wasp.watch.drawable
        hi =  wasp.system.theme('bright')
        prompt = "user@watch:~ $"

        draw.set_font(fonts.sans18)

        if redraw:
            now = wasp.watch.rtc.get_localtime()
            draw.fill()
            wasp.system.bar.draw()

            # Hour Labels
            draw.string("8", 68, 65)
            draw.string("4", 97, 65)
            draw.string("2", 127, 65)
            draw.string("1", 155, 65)

            # Min Labels
            draw.string("32", 32, 155)
            draw.string("16", 62, 155)
            draw.string("8", 97, 155)
            draw.string("4", 127, 155)
            draw.string("2", 157, 155)
            draw.string("1", 186, 155)
        else:
            now = wasp.system.bar.update()
            if not now or self._min == now[4]:
                # Skip the update
                return

        self._draw_clock(draw, now, 90, 90)

        draw.string(self._day_string(now), 0, 200, width=240)

        self._min = now[4]
