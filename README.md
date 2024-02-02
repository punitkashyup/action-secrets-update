# Update Secret Action

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/<your-username>/update-secret-action/Release?label=Release&logo=github)
![GitHub](https://img.shields.io/github/license/<your-username>/update-secret-action)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/<your-username>/update-secret-action?logo=github)

A GitHub Action to easily update a secret in your repository using strong encryption.

## Features

- Securely update secrets in your GitHub repository.
- Uses PyNaCl for encryption.
- Straightforward setup and usage.

## Usage

```yaml
name: Update Secret

on:
  push:
    branches:
      - main

jobs:
  update_secret:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Update Secret
      uses: punitkashyup/update-secret-action@v1
      with:
        repository_owner: ${{ secrets.REPOSITORY_OWNER }}
        repository_name: ${{ secrets.REPOSITORY_NAME }}
        secret_name: ${{ secrets.SECRET_NAME }}
        new_secret_value: ${{ secrets.NEW_SECRET_VALUE }}
        github_token: ${{ secrets.GITHUB_TOKEN }}
