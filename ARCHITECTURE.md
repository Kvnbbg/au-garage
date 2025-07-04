# Architecture
     ```mermaid
     graph TD
         A[User] --> B[Load Balancer]
         B --> C[Flask App]
         C --> D[PostgreSQL]
         C --> E[Google AI API]
