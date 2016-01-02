DROP TABLE IF EXISTS tasks;
CREATE TABLE tasks (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	title TEXT NOT NULL,
	description TEXT,
	date_of_creation TEXT NOT NULL,
	start_date TEXT,
	end_date TEXT,
	execution_time FLOAT
);
