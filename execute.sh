source <(grep -v '^#' _env-postgres.env | sed -E 's|^(.+)=(.*)$|: ${\1=\2}; export \1|g')
source <(grep -v '^#' _backend.env | sed -E 's|^(.+)=(.*)$|: ${\1=\2}; export \1|g')
cd app
uvicorn main:app --host 127.0.0.1 --port $INTERNAL_PORT