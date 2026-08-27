import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

tabs = re.findall(r'id=["\']tab-([^"\']+)["\']', html)
views = re.findall(r'id=["\']view-([^"\']+)["\']', html)
print('Tabs found:', tabs)
print('Views found:', views)
