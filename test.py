path_server = '/home/arkaeologic/arktic/woot/data/'
path_down = '/Users/nicholaspiano/code/arktic/woot/data/'
full_path_server = '/home/arkaeologic/arktic/woot/data/sdg/Jan2015/Log/2014/10October/20/bshoscar25PCI/305-189-10202014-144321062-20141020144523.wav'
full_path_down = '/Users/nicholaspiano/code/arktic/woot/data/sdg/Jan2015/Log/2014/10October/20/bshoscar25PCI/305-189-10202014-144321062-20141020144523.wav'

import os

wav_file_path = os.path.join(path_server, full_path_down[len(path_down):])

print(wav_file_path)
print(full_path_server)
