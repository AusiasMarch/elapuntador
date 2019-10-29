source <(grep -v '^#' env-postgres.env | sed -E 's|^(.+)=(.*)$|: ${\1=\2}; export \1|g')
source <(grep -v '^#' backend.env | sed -E 's|^(.+)=(.*)$|: ${\1=\2}; export \1|g')
uvicorn app/main:app --host 127.0.0.1 --port $INTERNAL_PORT