source <(grep -v '^#' env-postgres.env | sed -E 's|^(.+)=(.*)$|: ${\1=\2}; export \1|g')
source <(grep -v '^#' backend.env | sed -E 's|^(.+)=(.*)$|: ${\1=\2}; export \1|g')