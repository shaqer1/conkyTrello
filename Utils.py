class Utils:
    def getColors(self, color='NOCOLOR', s=''):
        if color == 'red':
            return '${color red}' + s + '$color'
        elif color == 'yellow':
            return '${color yellow}' + s + '$color'
        elif color == 'blue':
            return '${color blue}' + s + '$color'
        elif color == 'green':
            return '${color green}' + s + '$color'
        elif color == 'purple':
            return '${color #6a0dad}' + s + '$color'
        elif color == 'orange':
            return '${color #ffa500}' + s + '$color'
        elif color == 'NOCOLOR':
            return s
    def addLabels(self, labels):
        s=''
        for lb in labels:
            if lb['color'] != None:
                s += self.getColors(lb['color'], '■')
        return s