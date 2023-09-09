# i have a directory called domain_directory, in the directory have a lot directory, for the file in the same directory,
# the files are a lot of request's response as txt file, Only draw the home page relationship diagram
# According to the out-degree and in-degree, draw a map of the relationship between provinces and cities across the country. Analyze which types of nodes are more important.
# #


# i have store a lot of request's response as txt file, Analyze the inefficiency of website links
# Analyze the invalidity of the links (internal and external links) of the website on the homepage, including domain name resolution and web page content, etc.
# Compare by quantity + ratio.
# Number and distribution of backlinks


import os
import re
import networkx as nx
import matplotlib.pyplot as plt


def draw_relationship_diagram(domain_directory):
    # Iterate over the subdirectories in the domain directory
    for domain_name in os.listdir(domain_directory):
        domain_dir = os.path.join(domain_directory, domain_name)
        if os.path.isdir(domain_dir):
            G = nx.DiGraph()
            G.add_node(domain_name)

            # Iterate over the text files in the domain directory
            for filename in os.listdir(domain_dir):
                if filename.endswith(".txt"):
                    filepath = os.path.join(domain_dir, filename)
                    print(filepath)
                    # Extract the domain from the filename
                    match = re.search(r"^(.*)\.txt$", filename)
                    if match:
                        domain = match.group(1)
                        print(domain)
                        G.add_node(domain)
                    else:
                        print(f"Invalid filename format: {filename}")

                    # Read the contents of the text file
                    with open(filepath, "r", encoding="utf-8") as file:
                        content = file.read()

                    # Find the home page URL in the content
                    home_page_match = re.findall(
                        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", content)
                    print(home_page_match)
                    for url in home_page_match:
                        url_match = re.search(r"https?://([^/?]+)", url)
                        if url_match:
                            url_domain = url_match.group(1)
                            url_path = url.split('/', 3)[-1]  # Extract the path after the domain
                            # domain_with_path = f"{url_domain}/{url_path}"
                            # Add an edge to the graph connecting the domain to the home page URL
                            G.add_edge(domain, url_domain)
                            G.add_node(url_domain)

            # Calculate the in-degree and out-degree centrality measures
            in_degree_centrality = nx.in_degree_centrality(G)
            out_degree_centrality = nx.out_degree_centrality(G)

            # Sort the nodes by out-degree centrality and select the top 10 nodes
            sorted_nodes = sorted(G.nodes(), key=out_degree_centrality.get, reverse=True)[:10]

            # Create a subgraph with the top 10 nodes
            subgraph = G.subgraph(sorted_nodes)

            # Draw the graph with node sizes based on the in-degree and out-degree centrality
            pos = nx.spring_layout(subgraph)
            node_size = [10000 * in_degree_centrality[node] for node in subgraph.nodes()]
            node_color = [out_degree_centrality[node] for node in subgraph.nodes()]

            plt.figure(figsize=(12, 8), dpi=300)
            nx.draw_networkx(
                subgraph,
                pos=pos,
                with_labels=True,
                node_size=node_size,
                node_color=node_color,
                cmap=plt.cm.Blues,
                alpha=0.7,
                font_size=8,
                font_color="black",
                edge_color="gray",
                width=0.2,
            )

            # Add a colorbar
            sm = plt.cm.ScalarMappable(cmap=plt.cm.Blues)
            sm.set_array([])
            plt.colorbar(sm, label="Out-degree Centrality")

            plt.title(f"Home Page Relationship Diagram - {domain_name}")
            plt.axis("off")

            # Create the subdirectory for the output PNG file if it doesn't exist
            os.makedirs('relationship_result', exist_ok=True)

            # Save the diagram as PNG in the subdirectory with the same name as the subdirectory
            output_filename = os.path.join('relationship_result', f"{domain_name}.png")
            plt.savefig(output_filename, dpi=300)


# Specify the directory where the domain subdirectories are stored
domain_directory = "./domain_directory"

# Draw the home page relationship diagram for each subdirectory
draw_relationship_diagram(domain_directory)
