import networkx as nx

def filter_state_hash_percentage(df, p=0.34):
    state_hash_list = df['state_hash'].value_counts().sort_values(ascending=False).index.to_list()
    # get 34% number of blk in given batch
    total_unique_blk = df['block_producer_key'].nunique()
    percentage_result = round(total_unique_blk * p, 2)
    good_state_hash_list = list()
    for s in state_hash_list:
        blk_count = df[df['state_hash'] == s]['block_producer_key'].nunique()
        # check blk_count for state_hash submitted by blk least 34%
        if blk_count >= percentage_result:
            good_state_hash_list.append(s)
    return good_state_hash_list


def create_graph(batch_df, p_selected_node_df, c_selected_node, p_map):
    batch_graph = nx.DiGraph()
    parent_hash_list = batch_df['parent_state_hash'].unique()
    state_hash_list = set(list(batch_df['state_hash'].unique()) + list(p_selected_node_df['state_hash'].values))
    selected_parent = [parent for parent in parent_hash_list if parent in state_hash_list]
    """ t1=[w[42:] for w in list(p_selected_node_df['state_hash'].values)]
    t2=[w[42:] for w in c_selected_node]
    t3=[w[42:] for w in state_hash_list]
    batch_graph.add_nodes_from(t1)
    batch_graph.add_nodes_from( t2)
    batch_graph.add_nodes_from(t3) """

    batch_graph.add_nodes_from(list(p_selected_node_df['state_hash'].values))
    batch_graph.add_nodes_from(c_selected_node)
    batch_graph.add_nodes_from(state_hash_list)

    for row in batch_df.itertuples():
        state_hash = getattr(row, 'state_hash')
        parent_hash = getattr(row, 'parent_state_hash')

        if parent_hash in selected_parent:
            batch_graph.add_edge(parent_hash, state_hash)

    #  add edges from previous batch nodes
    batch_graph.add_edges_from(p_map)

    return batch_graph