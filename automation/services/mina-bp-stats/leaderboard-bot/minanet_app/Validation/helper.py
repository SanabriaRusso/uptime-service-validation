
def filter_state_hash_percentage(df, p=50):
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