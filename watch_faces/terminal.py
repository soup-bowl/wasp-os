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
        lo =  wasp.system.theme('mid')
        mid = draw.lighten(lo, 1)

        now = wasp.watch.rtc.get_localtime()
        if redraw:
            draw.fill()
        else:
            now = wasp.watch.rtc.get_localtime()
            #if not now or self._min == now[4]:
            #    return
        
        draw.set_font(fonts.sans18)

        start = 60

        draw.set_color(hi)
        draw.string("user@watch:~ $ now", 0, (start))
        draw.string("[TIME]", 0, (start + 20))
        draw.string("[DATE]", 0, (start + 40))
        draw.string("[BATT]", 0, (start + 60))
        draw.string("[STAT]", 0, (start + 80))
        draw.string("user@watch:~ $", 0, (start + 100))

        draw.set_color(COLORS[0])
        draw.string(self._time_string(now), 80, (start + 20))
        draw.set_color(COLORS[1])
        draw.string(self._day_string(now), 80, (start + 40))
        draw.set_color(COLORS[2])
        draw.string(str(watch.battery.level()), 80, (start + 60))
        draw.set_color(COLORS[5])
        draw.fill(x=80, y=(start + 80), w=80, h=20)
        draw.string("Connected" if wasp.watch.connected() else "Disconnected", 80, (start + 80))

        # Record the minute that is currently being displayed
        self._min = now[4]
