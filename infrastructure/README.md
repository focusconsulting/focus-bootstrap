# Infrastructure

## Developer Setup

TBD

## Mock external APIS

The project relies on several external APIs that are not readily accessible from a local development environment so a mock server is used to support making changes.

This mock works by loading in WSDLs and OpenAPI specs into a tool called [Imposter](https://docs.imposter.sh/).

These mocks are configured by `*-config.yaml` files that exist in `mocks/imposter`. See [the configuration guide](https://docs.imposter.sh/configuration/) for more details on how to adjust how these mocks work
