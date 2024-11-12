# Bootstrap

## Table of contents

-   [Documentation](./README.md#documentation)
-   [Developer Setup](./README.md#developer-setup)
    -   [API](./api/README.md#developer-setup)
    -   [Client](./client/README.md#developer-setup)
    -   [Infrastructure](./infrastructure/README.md#developer-setup)
-   [Using DevContainers](./README.md#using-devcontainers)
-   [Directories](./README.md#directory-structure)

## Documentation

Technical documentation for this project can be found in [docs](./docs/README.md) and includes information around the various technical decisions that have been made on the project as well as any standard operating procedures.

## Developer Setup

### IDE

Any idea can be used, but it is recommended to use [VS Code](https://code.visualstudio.com/download) as it has been verified to work the variety of tooling and has first-party plugins for the variety of build tools used by the repository.

The repository comes with settings configured as well as a recommended set of plugins to [install](.vscode/README.md#plugins-to-install)

1. Install the relevant dependencies
2. Set up the pre-commit hooks
3. Run `npm start`
4. Verify that the expected urls are available
    - [Swagger UI for API](http://localhost:8000/v1/ui)
    - [Swagger UI for the mocked external APIs](http://localhost:8080/_spec/)
5. Navigate to the other directories to setup the relevant pieces of the application

### Installing dependencies

In order to work on this repository there are a handful of tools that you will need to install.

This project requires both python and nodejs and these can be easily installed and managed with a tool called [asdf](https://asdf-vm.com/) and the relevant plugins

-   [asdf-nodejs](https://github.com/asdf-vm/asdf-nodejs)
-   [asdf-python](https://github.com/asdf-community/asdf-python)

Dependencies to install:

-   nodejs >=20
-   python >=3.12
-   [poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)
-   [docker](https://docs.docker.com/engine/install/)

### Pre-commit hooks

This project makes use of a pre-commit hook that will check any staged files for linting and formatting and prevent a commit if anything does not pass. In order to have the commit hooks, you'll need to run in the root directory.

```sh
npm install
```

## Using DevContainers

This repository supports development using [development containers](https://containers.dev/) removing the need to install any other dependencies on your system
and this tool is supported by a wide variety of IDEs. This removes the need to install any dependencies locally and instead your development will happen inside the
container. IDEs like VSCode will then seamlessly tunnel into the container so that the experience would be the same as if the tools were installed natively.

_This is highly recommend if you are developing on a Windows or Linux machine_

## Directory Structure

```
└── docs              Technical documentation for the project
└── api               The API
└── client            The user experience that interacts with the API
└── infrastructure    Infrastructure config and mock external API configuration
```
