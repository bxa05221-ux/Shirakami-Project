# Matome Execution Boundary v0.1

status: experimental

## Flow

    Matome YAML-shaped document
              |
              v
        Matome Loader
              |
              v
       Context + Protocol
              |
              v
          Runtime
              |
              v
          Evidence

## Rule

The Matome document is now an executable starting boundary for the JOUMON PoC. It defines the semantic statement, primary purpose and Human Gate constraints used to construct Context and Protocol inputs.

## Important distinction

The loader does not let Matome grant authority. Human Gate remains a separate final decision boundary.

## Parser status

v0.1 uses a constrained mapping interface rather than a YAML parser dependency. A canonical YAML parser can replace the loader implementation without changing the semantic contract.
