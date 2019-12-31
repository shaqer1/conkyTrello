from datetime import datetime, timedelta, timezone
import pytz

class Utils:
    def getColors(self, color='NOCOLOR', s=''):
        if color == 'red':
            return '${color red}' + s + '${color}'
        elif color == 'yellow':
            return '${color yellow}' + s + '${color}'
        elif color == 'blue':
            return '${color blue}' + s + '${color}'
        elif color == 'green':
            return '${color green}' + s + '${color}'
        elif color == 'purple':
            return '${color #6a0dad}' + s + '${color}'
        elif color == 'orange':
            return '${color #ffa500}' + s + '${color}'
        elif color == 'NOCOLOR':
            return s
        else:
            return s
    def addLabels(self, labels):
        s=''
        for lb in labels:
            if lb['color'] != None:
                s += self.getColors(lb['color'], '■')
        return s
    def getFont(self, fontClass='', s=''):
        if fontClass == 'title':
            return '${font DejaVu Sans Mono:bold:size=12}' + s + '${font}'
        elif fontClass == 'body':
            return '${font DejaVu Sans Mono:bold:size=10}' + s + '${font}'
        else:
            return s

    def processDate(self, date):
        s=''
        now=datetime.now()
        d=date.replace(tzinfo=None)
        if now-timedelta(hours=24) <= d <= now+timedelta(hours=24): #date - today < 24 hours
            diff = now - d if now > d else d - now
            s+= str(divmod(diff.seconds, 3600)[0]) + ' hrs'
        elif now-timedelta(days=14) <= d <= now+timedelta(days=14): #date - today < 2 weeks
            diff = now - d if now > d else d - now
            s+= str(diff.days) + ' days'
        else:
            diff = now - d if now > d else d - now
            s+= str(divmod(diff.days, 7)[0]) + ' wks'
        s='${font Symbola} 📅$font ' + s
        if d < now:
            s=self.getColors('red', s)
        elif d <= now+timedelta(hours=24):
            s=self.getColors('yellow', s)
        else:
            s=self.getColors('green', s)
        return s