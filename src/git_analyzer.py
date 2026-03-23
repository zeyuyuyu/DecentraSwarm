import git
import matplotlib.pyplot as plt
import networkx as nx

def analyze_commit_history(repo_path):
    # Create a Git repository object
    repo = git.Repo(repo_path)

    # Get the commit history
    commits = list(repo.iter_commits())

    # Create a directed graph
    G = nx.DiGraph()

    # Add nodes (commits) to the graph
    for commit in commits:
        G.add_node(commit.hexsha, author=commit.author.name, date=commit.authored_date)

    # Add edges (commit relationships) to the graph
    for i in range(1, len(commits)):
        G.add_edge(commits[i].hexsha, commits[i-1].hexsha)

    # Visualize the commit history
    pos = nx.spring_layout(G)
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', font_size=8)
    plt.title('Commit History Visualization')
    plt.show()

    return G
