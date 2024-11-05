import json
import datetime

data = json.load(open('data/all_cres.json'))['data']
source_link = 'https://github.com/OWASP/OpenCRE'
dateString = datetime.date.today().strftime('%Y-%m-%d')

links_text = ''
links = []
links_map = {}

for doc in data:
    if doc.get('name'):
        for link in doc['links']:
            if link.get('document'):
                doc_node = '';
                if (doc.get('id')): doc_node += doc['id'] + ' '
                if (doc.get('sectionID')): doc_node += '['
                doc_node += doc['name']
                if doc.get('section'): doc_node += ' ' + doc['section']
                if doc.get('sectionID'): doc_node += ' ' + doc['sectionID']

                if (doc.get('sectionID')): doc_node += ']'

                link_node = '';
                if (link['document'].get('id')): link_node += link['document']['id']
                if (link['document'].get('sectionID')): link_node += '['
                link_node += link['document']['name']
                if link['document'].get('section'): link_node += ' ' + link['document']['section']
                if link['document'].get('sectionID'): link_node += ' ' + link['document']['sectionID']
                if (link['document'].get('sectionID')): link_node += ']'

                link_id_1 = doc_node + '::' + link_node
                link_id_2 = link_node + '::' + doc_node
                if not links_map.get(link_id_1) and not links_map.get(link_id_2):
                    links_map[link_id_1] = {'source': doc_node, 'target': link_node, 'count': 1}
                    links_text += '"' + doc_node + '" -- "' + link_node + '";\n'
                    links.append(links_map[link_id_1])
                elif links_map.get(link_id_1):
                    links_map[link_id_1]['count'] += 1
                elif links_map.get(link_id_2):
                    links_map[link_id_2]['count'] += 1

with open('docs/index.html', 'w') as html_file:
    template = open('templates/overview-contains.html').read();
    html_file.write(template
                    .replace('${date}', dateString)
                    .replace('${source_link}', source_link)
                    .replace('${data}', json.dumps(data)))

with open('docs/overview-summary.html', 'w') as html_file:
    template = open('templates/overview-summary.html').read();
    html_file.write(template
                    .replace('${date}', dateString)
                    .replace('${source_link}', source_link)
                    .replace('${data}', json.dumps(data)))

with open('docs/visuals/docs-graph.dot', 'w') as html_file:
    template = open('templates/visuals/graphviz.dot').read();
    html_file.write(template
                    .replace('${nodes}', '')
                    .replace('${links}', links_text))

with open('docs/visuals/force-graph-3d.html', 'w') as html_file:
    template = open('templates/visuals/force-graph-3d.html').read();
    html_file.write(template
                    .replace('${links}', json.dumps(links)))

with open('docs/visuals/circles.html', 'w') as html_file:
    template = open('templates/visuals/circles.html').read();
    html_file.write(template
                    .replace('${links}', json.dumps(data)))
