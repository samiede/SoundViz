import matplotlib.pylab as plt
import matplotlib.colors
import numpy as np
import matplotlib.cm as cm
import wave
import sys
import copy

#color mapping
#           darks       mids      special    highlights
greens = ['#24874c', '#3ad779', '#53efab', '#e2ef53']
blues = ['#244987', '#3a79d7', '#6def53', '#ef53ed']
reds = ['#872424', '#d73a54', '#ef9153', '#53d7ef']
darks = ['#000000', '#808080', '#ffffff', '#c40000']
inverts = ['#ffffff', '#feffb2', '#ffffff', '#9a9fff']
#srg = ['#000000', '#d73a54', '#ffffff', '#ffd900']
srg = ['#ffd900', '#d73a54', '#ffffff', '#000000']



schemes = [greens, blues, reds, darks, inverts, srg]

#default values
fileName = str('')
number_of_samples = 200
linewidth = 5
scheme_index = 0
background = 'white'
alpha = 0.8

if len(sys.argv) > 5:
    print 'Invalid Number of arguments!'
    print 'Usage: soundViz.py [filename][Number of Samples] [Linewidth] [Colorscheme]'
    sys.exit()

elif len(sys.argv) == 5:
    fileName = sys.argv[1]
    number_of_samples = int(sys.argv[2])
    linewidth = int(sys.argv[3])
    if sys.argv[4] == 'greens':
        scheme_index = 0
    elif sys.argv[4] == 'blues':
        scheme_index = 1
    elif sys.argv[4] == 'reds':
        scheme_index = 2
    elif sys.argv[4] == 'darks':
        scheme_index = 3
    elif sys.argv[4] == 'inverts':
        scheme_index = 4
        background = 'black'
        alpha = 1.0
    elif sys.argv[4] == 'srg':
        scheme_index = 5
    else:
        print 'No such color scheme!'
        print 'Schemes available:'
        print '\'greens\'(default), \'blues\', \'darks\', \'inverts\' and \'reds\''
        print 'Using greens'
        scheme_index = 0
elif len(sys.argv) == 4:
        fileName = sys.argv[1]
        number_of_samples = int(sys.argv[2])
        linewidth = int(sys.argv[3])
elif len(sys.argv) == 3:
        fileName = sys.argv[1]
        number_of_samples = int(sys.argv[1])
elif len(sys.argv) == 2:
        fileName = sys.argv[1]
else:
        print 'No file specified'
        sys.exit(0)




colorscheme = copy.deepcopy(schemes[scheme_index])


darks = matplotlib.colors.colorConverter.to_rgb(colorscheme[0])
mids = matplotlib.colors.colorConverter.to_rgb(colorscheme[1])
specials = matplotlib.colors.colorConverter.to_rgb(colorscheme[2])
highlights = matplotlib.colors.colorConverter.to_rgb(colorscheme[3])

#get raw audio vom wave file
spf = wave.open(fileName, 'r')
signal = spf.readframes(-1)
signal = np.fromstring(signal, 'Int16')

sample_rate = len(signal)/number_of_samples

color_thresh = max(signal)/2
color_thresh2 = max(signal)/4

colors = []
for entry in range(len(signal)):
    colors.append(0)
    if abs(signal[entry]) > color_thresh2:
        colors[entry] = highlights
    elif abs(signal[entry]) < 500:
        colors[entry] = darks
    else:
        colors[entry] = mids


#triming signal
trim_signal = []
trim_colors = []
step = 0
for i in range(number_of_samples):
    trim_signal.append(signal[step])
    trim_colors.append(colors[step])
    step += sample_rate

#build axis
x = []
for i in range(len(trim_signal)):
    x.append(i)
y = [0] * len(x)


params = matplotlib.figure.SubplotParams(left = 0.2, bottom = 0.2, right = None, top=None, wspace=None, hspace=None)

fig = plt.figure()
fig.subplots_adjust(left = 0.02, bottom = 0.02, right = 0.98, top = 0.98)
fig.set_facecolor(background)
a,b,c = plt.errorbar(x, y, yerr = trim_signal, xerr = None, elinewidth = linewidth, fmt = 'none', barsabove = False, mew = 0, alpha = alpha, antialiased = True)
c[0].set_color(trim_colors)
plt.axis('off')
fig.savefig('soundViz.png', dpi = 300, facecolor = background)
plt.show()
