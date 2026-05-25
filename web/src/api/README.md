# api

API wrappers for existing backend endpoints.

Rules:

- preserve existing endpoint paths;
- include CSRF for mutating actions;
- use preview endpoints before apply endpoints;
- keep response-shape adapters local and explicit.

