# OpenAPI Specification Helper

Help me create or review an OpenAPI 3.1 specification.

## Task

[DESCRIBE WHAT YOU WANT TO CREATE OR REVIEW]

## Guidelines

When generating or reviewing OpenAPI specs, apply these conventions:

### Structure

```yaml
openapi: "3.1.0"
info:
  title: <Service Name> API
  version: "1.0.0"
  description: |
    Brief description of the API.
  contact:
    name: API Support
    url: https://github.com/abuxton
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://api.staging.example.com/v1
    description: Staging

paths:
  /resources:
    get:
      operationId: listResources
      summary: List all resources
      tags: [resources]
      parameters:
        - $ref: '#/components/parameters/PageParam'
        - $ref: '#/components/parameters/LimitParam'
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ResourceList'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '500':
          $ref: '#/components/responses/InternalServerError'

components:
  schemas:
    Resource:
      type: object
      required: [id, name]
      properties:
        id:
          type: string
          format: uuid
          description: Unique identifier
          readOnly: true
        name:
          type: string
          description: Human-readable name
          minLength: 1
          maxLength: 255

  responses:
    BadRequest:
      description: Invalid request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    Unauthorized:
      description: Authentication required
    InternalServerError:
      description: Unexpected server error

  parameters:
    PageParam:
      name: page
      in: query
      schema:
        type: integer
        minimum: 1
        default: 1
    LimitParam:
      name: limit
      in: query
      schema:
        type: integer
        minimum: 1
        maximum: 100
        default: 20

  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

### Checklist

- [ ] `operationId` set for every operation (camelCase)
- [ ] All operations have `summary` and `tags`
- [ ] Request bodies use `$ref` to component schemas
- [ ] All 4xx and 5xx responses documented
- [ ] Parameters documented with type, format, and description
- [ ] Reusable components extracted to `components/`
- [ ] Spec validates with `spectral lint` or `redocly lint`
