# import pygraphviz as pgv
# from IPython.display import Image
#
# # Create a directed graph
# G = pgv.AGraph(strict=True, directed=True)
#
# # Add nodes and edges
# nodes = [
#     'Web Application', 'Third Party JS Library', 'Mobile Client Support',
#     'Access Speed', 'Status', 'Assistance for the Elderly', 'Webpage',
#     'Version', 'Vulnerability', 'Evidence', 'Solution',
#     'Domain', 'Nameserver 1', 'Nameserver 2', 'Nameserver N',
#     'Webpage Total Links', 'HTTP Links', 'HTTPS Links', 'Invalid Links',
#     'ICP License', 'Owner', 'IP 1', 'IP 2', 'Port 53 (Open)', 'Port 8080 (Open)',
#     'Location', 'ASN', 'DNSSEC Support', 'EDNS Support', 'TLS Support',
#     'TCP Support', 'DNS Records', 'CNAME Records', 'SOA Records',
#     'A Records', 'AAAA Records', 'XXX Records', 'Support Something',
#     'CDN Service', 'CA', 'Subject', 'Issuer'
# ]
#
# edges = [
#     ('Web Application', 'Third Party JS Library'),
#     ('Web Application', 'Mobile Client Support'),
#     ('Web Application', 'Access Speed'),
#     ('Web Application', 'Status'),
#     ('Web Application', 'Assistance for the Elderly'),
#     ('Web Application', 'Webpage'),
#     ('Third Party JS Library', 'Version'),
#     ('Third Party JS Library', 'Vulnerability'),
#     ('Vulnerability', 'Evidence'),
#     ('Vulnerability', 'Solution'),
#     ('Domain', 'Nameserver 1'),
#     ('Domain', 'Nameserver 2'),
#     ('Domain', 'Nameserver N'),
#     ('Domain', 'Webpage Total Links'),
#     ('Webpage', 'HTTP Links'),
#     ('Webpage', 'HTTPS Links'),
#     ('Webpage', 'Invalid Links'),
#     ('Domain', 'ICP License'),
#     ('Domain', 'Owner'),
#     ('Domain', 'IP 1'),
#     ('Domain', 'IP 2'),
#     ('Nameserver 1', 'Location'),
#     ('Nameserver 1', 'ASN'),
#     ('Nameserver 2', 'Port 53 (Open)'),
#     ('Nameserver 2', 'Port 8080 (Open)'),
#     ('Nameserver 2', 'DNSSEC Support'),
#     ('Nameserver 2', 'EDNS Support'),
#     ('Nameserver 2', 'TLS Support'),
#     ('Nameserver 2', 'TCP Support'),
#     ('Nameserver 2', 'DNS Records'),
#     ('DNS Records', 'CNAME Records'),
#     ('DNS Records', 'SOA Records'),
#     ('DNS Records', 'A Records'),
#     ('DNS Records', 'AAAA Records'),
#     ('DNS Records', 'XXX Records'),
#     ('XXX Records', 'Support Something'),
#     ('Domain', 'CDN Service'),
#     ('Domain', 'CA'),
#     ('CA', 'Subject'),
#     ('CA', 'Issuer'),
# ]
#
# G.add_nodes_from(nodes)
# G.add_edges_from(edges)
#
# # Generate a PNG file
# file_path = "graph.png"
# G.draw(file_path, format='png', prog='dot')
#
# # Display the graph
# Image(file_path)
