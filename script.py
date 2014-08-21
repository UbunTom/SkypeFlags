import Image, os, sys

if len(sys.argv) < 2:
    print("Please specify a file name")

im=Image.open(sys.argv[1])

pixels = list(im.getdata())
width, height = im.size
pixels = [pixels[i * width:(i + 1) * width] for i in xrange(height)]

flags_w = width//16
flags_h = height//11

print(width, height)

class Flag:

    def __init__(self, fname):
        im = Image.open(fname);
        self.flagid = "(flag:"+fname[7:9].upper()+")"

        pixels = list(im.getdata())
        width, height = 16, 11
        self.buffer = [pixels[i * width:(i + 1) * width] for i in xrange(height)]

    def correlate(self, baseImage, x, y, max):
        sum = 0
        for pX in range(0, 15):
            for pY in range(0, 10):
                base = baseImage[pY + y*11][pX + x*16]
                comp = self.buffer[pY][pX]

                dRed = base[0]-comp[0];
                dGreen = base[1]-comp[1];
                dBlue = base[2]-comp[2];

                sum += dRed**2 + dGreen**2 + dBlue**2;

            if sum > max:
                return sum;

#print(self.flagid + " " + str(sum))

        return sum;

flags = []
for file in os.listdir("images"):
    flags.append(Flag("images/"+file))

print("Loaded flags");

print("Generating " + str(flags_w) + " by " + str(flags_h) + " flags")
output = ""
for fY in range(0, flags_h):
    for fX in range(0, flags_w):
        sum = 2**31
        stri = ""

        for flag in flags:
            test = flag.correlate(pixels, fX, fY, sum)
            if test < sum:
                sum = test
                stri = flag.flagid

        output+=stri;
    output+="\n"

    print(str(int(100*(fY+1) / float(flags_h))) + "%")

print(output)
