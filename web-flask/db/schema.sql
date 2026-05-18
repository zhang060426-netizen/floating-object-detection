CREATE TABLE IF NOT EXISTS user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  real_name TEXT,
  phone TEXT,
  email TEXT,
  avatar_bucket TEXT,
  avatar_object_key TEXT,
  role INTEGER NOT NULL DEFAULT 0,
  status INTEGER NOT NULL DEFAULT 1,
  create_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  update_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS models (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  dataset_id TEXT,
  base_model TEXT,
  status INTEGER DEFAULT 1,
  model_bucket TEXT,
  model_object_key TEXT,
  weight_path TEXT,
  train_images TEXT,
  train_files TEXT,
  is_dev_placeholder INTEGER DEFAULT 1,
  create_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  update_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS detection_records (
  id TEXT PRIMARY KEY,
  user_id INTEGER NOT NULL,
  model_id TEXT NOT NULL,
  original_image_bucket TEXT NOT NULL,
  original_image_object_key TEXT NOT NULL,
  result_image_bucket TEXT,
  result_image_object_key TEXT,
  detection_result TEXT,
  confidence_threshold REAL DEFAULT 0.5,
  create_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT,
  description TEXT,
  enhanced_image_bucket TEXT,
  enhanced_image_object_key TEXT,
  analysis_result TEXT,
  suggestions TEXT,
  FOREIGN KEY(user_id) REFERENCES user(id),
  FOREIGN KEY(model_id) REFERENCES models(id)
);

CREATE TABLE IF NOT EXISTS detection_crops (
  id TEXT PRIMARY KEY,
  record_id TEXT NOT NULL,
  object_index INTEGER NOT NULL,
  class_name TEXT NOT NULL,
  confidence REAL NOT NULL,
  bbox TEXT NOT NULL,
  image_bucket TEXT NOT NULL,
  image_object_key TEXT NOT NULL,
  create_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(record_id) REFERENCES detection_records(id)
);

CREATE INDEX IF NOT EXISTS idx_detection_records_user_time ON detection_records(user_id, create_time DESC);
CREATE INDEX IF NOT EXISTS idx_detection_records_model ON detection_records(model_id);
