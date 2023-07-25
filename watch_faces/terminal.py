import wasp
import watch
import fonts

COLORS = [0x166A,0x03FF,0x3BCA,0xE98E,0xE982,0x041F]

class TerminalApp():
    NAME = 'Terminal'

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
    
    def _time_string(self, now):
        return '{}:{}:{}'.format(str(now[3]).zfill(2), str(now[4]).zfill(2), str(now[5]).zfill(2))

    def _day_string(self, now):
        return '{}-{}-{}'.format(now[0], str(now[1]).zfill(2), str(now[2]).zfill(2))

    def _draw(self, redraw=False):
        draw = wasp.watch.drawable
        hi =  wasp.system.theme('bright')
        prompt = "user@watch:~ $"

        now = wasp.watch.rtc.get_localtime()
        if redraw:
            draw.fill()
        else:
            now = wasp.watch.rtc.get_localtime()
            if not now or self._sec == now[5]:
                return
        
        draw.set_font(fonts.sans18)

        start = 60
        label_x = 0
        text_x = 80
        gap = 20

        draw.set_color(hi)
        draw.string(prompt + " now", label_x, (start))
        draw.string("[TIME]", label_x, (start + (gap * 1)))
        draw.string("[DATE]", label_x, (start + (gap * 2)))
        draw.string("[BATT]", label_x, (start + (gap * 3)))
        draw.string("[STAT]", label_x, (start + (gap * 4)))
        draw.string(prompt, label_x, (start + (gap * 5)))

        draw.set_color(COLORS[0])
        draw.string(self._time_string(now), text_x, (start + (gap * 1)))
        draw.set_color(COLORS[1])
        draw.string(self._day_string(now), text_x, (start + (gap * 2)))
        draw.set_color(COLORS[2])
        draw.string("{}% {}".format(
            watch.battery.level(),
            " Charging" if watch.battery.charging() else "             "
        ), text_x, (start + (gap * 3)))
        draw.set_color(COLORS[5])
        draw.string("Connected     " if wasp.watch.connected() else "Disconnected", text_x, (start + (gap * 4)))

        self._sec = now[5]
