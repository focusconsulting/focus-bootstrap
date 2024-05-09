# Architecture Decision Record (ADR) - 001

## Title

Technical choices for the project

## Context

Before getting started on development, the project will need to have established which technologies will be used for development.

## Decision

The project will be broken down into two main pieces:

- An API layer that talks to a database and the external APIs that implements all the business logic
- A client that invokes the API layer and provides the user experience

### Further breakdown

- Python API layer
  - Web Framework: connexion
  - Database access: sqlalchemy
  - Database migrations: alembic
  - Validation: Pydantic
  - Mypy: Type checking
- Typescript Client
  - SPA Next.js application
  - USWDS React component library
  - Storybook

## Rationale

### API Layer

- Python was chosen as it is a well-supported language and has a large ecosystem and history of being used in production contexts. It is a strongly idiomatic language which means developers spend less time deciding the style in which to write functionality but can instead focus on implementing business logic. Additionally, the combination of a static checker MyPy and the flexibility of dynamically typed language at runtime provides an excellent combination of safety and flexibility for developers.
- One goal was to optimize how quickly APIs would be consumable by the client so that development on both layers can occur in parallel. To support this, connexion was chosen
  as it a spec-first framework that supports mocked responses out of the box. This allows developers to define the contracts for the API first and then separately work on implementing
  the python code while still allowing the client to consume the API.
- sqlalchemy, alembic, and pydantic are both well supported libraries that provide a large amount of built-in functionality that will eliminate the need for the team to write lots of boilerplate

### Client layer

- Similarly to python/mypy, Typescript is a well-supported language (backed by Microsoft) with a large ecosystem that provides the flexibility of static type checker while still ultimately operating as dynamically typed javascript code in the browser
- React/Next.js are extremely popular frontend frameworks used across the industry and are tools that the vast majority of frontend/fullstack developers will have experience with. Additionally, Next.js is feature-rich framework that provides a large amount of built-in functionality (i.e. routing) out of the box; additionally, it has support for being deployed as a server rather than a SPA if the team decides that is the better choice down the road
- USWDS React component library is wrapper around the USWDS that implements the components in React and will enable the team to quickly implement designs in the chosen framework
- Storybook is an excellent tool for enabling fast iterations on UIs and enables non-technical team members to use parts of the application without having to actually complete the business flows which can be tedious if there is a lot of required data setup
