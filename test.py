import os

for path, subs, files in os.walk('./woot/apps'):
  for file in files:
    if '.py' in file:
      with open(os.path.join(path, file), 'w') as f:
        f.write('\n')
