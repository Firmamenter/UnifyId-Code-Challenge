"""
Author: Da Chen
Date: Feb 10
"""
import wave
import struct
import urllib2
from PIL import Image


# Part 1. Get random number from API
r = list()
g = list()
b = list()
for i in range(128):
    # Send requests and fetch data
    rVal = urllib2.urlopen(
        "https://www.random.org/integers/?num=128&min=0&max=255&col=128&base=10&format=plain&rnd=new")
    gVal = urllib2.urlopen(
        "https://www.random.org/integers/?num=128&min=0&max=255&col=128&base=10&format=plain&rnd=new")
    bVal = urllib2.urlopen(
        "https://www.random.org/integers/?num=128&min=0&max=255&col=128&base=10&format=plain&rnd=new")
    # Store data in rgb channels
    nums = rVal.read()
    nums = nums.strip().split("\n")
    r.extend(nums[0].split("\t"))
    nums = gVal.read()
    nums = nums.strip().split("\n")
    g.extend(nums[0].split("\t"))
    nums = bVal.read()
    nums = nums.strip().split("\n")
    b.extend(nums[0].split("\t"))

r = map(int, r)
g = map(int, g)
b = map(int, b)


# Part 2. Create RGB Bitmap picture
img = Image.new('RGB', (128, 128), "black")
pixels = img.load()

# Set rgb values
for i in range(img.size[0]):
    for j in range(img.size[1]):
        pixels[i, j] = (r[i * 128 + j], g[i * 128 + j], b[i * 128 + j])

img.save('randomRGB.bmp')


# Part 3. Generate noise file
# Number of samples = 128 * 128 * 3
numOfSamples = 16384 * 3

# Use random number from Part 2
randNum = []
randNum.extend(r)
randNum.extend(g)
randNum.extend(b)

noise = wave.open('noise.wav', 'w')
noise.setparams((2, 2, 16384, 0, 'NONE', 'not compressed'))

values = []

for i in range(0, numOfSamples):
    value = randNum[i]
    packed_value = struct.pack('h', value)
    values.append(packed_value)
    values.append(packed_value)

valueStr = ''.join(values)
noise.writeframes(valueStr)

noise.close()