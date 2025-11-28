# API Development Plugin

REST API design, OpenAPI specifications, and backend architecture patterns.

## Installation

```bash
/plugin install api-development@cameron-tools
```

## Commands

### `/review.api`

Review API design for REST best practices, naming conventions, and OpenAPI compliance.

**Usage:**
```bash
/review.api
/review.api path/to/openapi.yaml
```

**Checks:**
- Naming conventions (snake_case fields, kebab-case URIs)
- Resource modeling
- HTTP methods and status codes
- Error handling (RFC 9457)
- Versioning strategy
- Pagination patterns

### `/review.architecture`

Review system architecture for consistency and patterns.

**Usage:**
```bash
/review.architecture
```

## Agents

### api-documenter

Create OpenAPI/Swagger specs, generate SDKs, and write developer documentation.

**Capabilities:**
- OpenAPI 3.0 specification creation
- SDK generation
- Developer documentation
- Versioning patterns
- Interactive docs

### backend-architect

Design RESTful APIs, microservice boundaries, and database schemas.

**Capabilities:**
- API design patterns
- Microservice architecture
- Database schema design
- Scalability patterns
- Performance optimization

### graphql-architect

Design GraphQL schemas, resolvers, and federation.

**Capabilities:**
- Schema design
- Resolver patterns
- N+1 query prevention
- Subscription implementation
- Federation setup

## Skills

### api-design

Comprehensive REST API design guidelines.

**Covers:**
- Naming conventions
- Resource modeling
- HTTP methods and status codes
- Error handling (RFC 9457)
- Versioning
- Pagination
- Common types (money, dates, etc.)

## Example Usage

### Review an API

```bash
/review.api
```

### Design a New API

```
"Use api-documenter to create an OpenAPI spec for a user management API"
```

### Architectural Review

```
"Use backend-architect to review our microservice boundaries"
```

## Works Well With

- **security-suite** - API security auditing
- **python-toolkit** / **typescript-toolkit** - Implementation
- **core-productivity** - Code review and commits
