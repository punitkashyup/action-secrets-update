FROM python:3.8-slim

LABEL "com.github.actions.name"="Update Secret Action"
LABEL "com.github.actions.description"="A GitHub Action to update a secret in a repository"
LABEL "com.github.actions.icon"="shield"
LABEL "com.github.actions.color"="blue"

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
