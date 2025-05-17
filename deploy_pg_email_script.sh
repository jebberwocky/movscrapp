# Define paths
SERVER_USER="root"  # Change this to your server username if needed
SERVER_HOST="157.245.49.95"  # Change this to your server hostname or IP
REMOTE_DIR="/mnt/volume_sgp1_01/script/pg_email_script"
LOCAL_SCRIPT_PATH="./pg_email_script.py"  # Current directory by default
LOCAL_CONFIG_PATH="./default.ini"  # Use first argument or default to current directory


scp "${LOCAL_SCRIPT_PATH}" "${SERVER_USER}@${SERVER_HOST}:${REMOTE_DIR}/pg_email_script.py"
scp "${LOCAL_CONFIG_PATH}" "${SERVER_USER}@${SERVER_HOST}:${REMOTE_DIR}/default.ini"


