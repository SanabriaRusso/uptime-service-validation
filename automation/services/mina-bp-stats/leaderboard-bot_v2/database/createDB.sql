--Need to check on this structure. Feels like some of these should be non-null.
DROP TABLE IF EXISTS bot_logs;
CREATE TABLE bot_logs (
	id SERIAL PRIMARY KEY, 
	name_of_file CHARACTER VARYING, 
	processing_time BIGINT, 
	files_processed INT, 
	file_timestamp TIMESTAMP, 
	batch_start_epoch BIGINT, 
	batch_end_epoch BIGINT
);

DROP TABLE IF EXISTS statehash;
CREATE TABLE statehash (
	id SERIAL PRIMARY KEY,
	values CHARACTER VARYING UNIQUE
);

DROP TABLE IF EXISTS botlogs_statehash;
CREATE TABLE botlogs_statehash (
	id SERIAL PRIMARY KEY,
	parent_statehash_id INT, 
	statehash_id INT, 
	weight INT NOT NULL, 
	bot_log_id int,
	CONSTRAINT fk_parent_statehash
		FOREIGN KEY(parent_statehash_id) 
		REFERENCES statehash(id),
	CONSTRAINT fk_statehash
		FOREIGN KEY(statehash_id) 
		REFERENCES statehash(id),
	CONSTRAINT fk_bot_log
		FOREIGN KEY(bot_log_id) 
		REFERENCES bot_logs(id)
);

DROP TABLE IF EXISTS nodes;
CREATE TABLE nodes (
	id SERIAL PRIMARY KEY,
	block_producer_key CHARACTER VARYING UNIQUE,
	updated_at TIMESTAMP NOT NULL,
	score INT,
	score_percent NUMERIC(6,2)
);

DROP TABLE IF EXISTS points;
CREATE TABLE points (
	id SERIAL PRIMARY KEY,
	file_name CHARACTER VARYING NOT NULL,
	file_timestamps TIMESTAMP NOT NULL, 
	blockchain_epoch BIGINT NOT NULL, 
	blockchain_height BIGINT NOT NULL,
    amount INT NOT NULL, 
	created_at TIMESTAMP NOT NULL,
	node_id int,
	bot_log_id int,
	statehash_id int
	CONSTRAINT fk_nodes
		FOREIGN KEY(node_id) 
		REFERENCES nodes(id),
	CONSTRAINT fk_bot_log
		FOREIGN KEY(bot_log_id) 
		REFERENCES bot_logs(id),
	CONSTRAINT fk_statehashes
		FOREIGN KEY(statehash_id) 
		REFERENCES statehash(id)
);

--Should some of these values be nullable? If uptime file doesn't pass validation, say?
DROP TABLE IF EXISTS uptime_file_history;
CREATE TABLE uptime_file_history (
	id SERIAL PRIMARY KEY,
	file_name CHARACTER VARYING, 
	receivedat TIMESTAMP NOT NULL,
	receivedfrom TIMESTAMP NOT NULL, 
	node_id INT NOT NULL, 
	block_statehash INT,
    parent_block_statehash INT 
	nodedata_blockheight BIGINT NOT NULL, 
	nodedata_slot BIGINT NOT NULL, 
	file_modified_at TIMESTAMP NOT NULL, 
	file_created_at TIMESTAMP NOT NULL, 
	file_generation TIMESTAMP NOT NULL,
    file_crc32c CHARACTER VARYING NOT NULL, 
	file_md5_hash CHARACTER VARYING NOT NULL,
	CONSTRAINT fk_nodes
		FOREIGN KEY(node_id) 
		REFERENCES nodes(id),
	CONSTRAINT fk_parent_statehash
		FOREIGN KEY(parent_statehash_id) 
		REFERENCES statehash(id),
	CONSTRAINT fk_statehash
		FOREIGN KEY(statehash_id) 
		REFERENCES statehash(id)
);

DROP TABLE IF EXISTS score_history;
CREATE TABLE score_history (
	id SERIAL PRIMARY KEY,
	node_id INT,
	score_at TIMESTAMP NOT NULL, 
	score INT NOT NULL, 
	score_percent NUMERIC(6,2) NOT NULL,
	CONSTRAINT fk_nodes
		FOREIGN KEY(node_id) 
		REFERENCES nodes(id)
);

-- Point Summary table that is auto-gen?
-- Looks like there's an apoch table as well, but can't find much detail.
