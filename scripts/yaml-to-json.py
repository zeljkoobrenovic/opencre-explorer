import yaml
import json
import os
import http.client

cres_root = '../data/cres/'
cres_files = [f for f in os.listdir(cres_root) if os.path.isfile(cres_root + f) and f.endswith('.yaml')]

cres = []

conn = http.client.HTTPSConnection('opencre.org');

for f in cres_files:
    print(f)
    with open(cres_root + f, 'r') as file:
        f_data = yaml.safe_load(file)
        url = 'https://opencre.org/rest/v1/id/' + f_data['id']
        print(url)
        conn.request("GET", '/rest/v1/id/' + f_data['id'], headers={"Host": 'opencre.org'})
        response = conn.getresponse()
        content = response.read().decode()
        if content and content != 'Resource Not found':
            data = json.loads(content)
            if (data.get('data')):
                print(data['data'])
                cres.append(data['data'])
                with open('../data/cres.json', 'w') as json_file:
                    json.dump(cres, json_file)
