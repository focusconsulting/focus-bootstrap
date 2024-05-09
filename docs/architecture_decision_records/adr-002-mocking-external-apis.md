# Architecture Decision Record (ADR) - 001

## Title

Mocking of the external APIS

## Context

This application will consume several external APIs that may not be available from day one and will likely never be available when developing locally.

## Decision

Use the tool Imposter to mock the external APIs

## Rationale

Imposter is a tool that can mock APIs when provide OpenApi specs or WSDLs which we have access to as part of this project. Additionally, the tool has rich support for complicated configuration of responses so that the team can create several different examples to test the workflows with different responses
