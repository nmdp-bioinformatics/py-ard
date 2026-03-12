# py-ard Architecture

This document provides a comprehensive overview of the py-ard project architecture, designed to help new developers understand the codebase and contribute effectively.

## Table of Contents

1. [Overview](#overview)
2. [High-Level Architecture](#high-level-architecture)
3. [Core Components](#core-components)
4. [Data Flow](#data-flow)
5. [Module Details](#module-details)
6. [Design Patterns](#design-patterns)
7. [Database Schema](#database-schema)
8. [Extension Points](#extension-points)

---

## Overview

`py-ard` is a Python library for HLA (Human Leukocyte Antigen) nomenclature reduction and manipulation. It reduces HLA typings to various resolution levels (G group, P group, lg, lgx, etc.) based on IPD-IMGT/HLA database releases.

**Key Features:**
- Multiple reduction strategies (G, P, lg, lgx, W, exon, U2, S)
- MAC code expansion and lookup
- Serology to allele mapping
- V2 to V3 allele conversion
- GL String processing
- CWD (Common and Well-Documented) reduction
- REST API service
- Command-line tools

---

## High-Level Architecture

```mermaid
graph TB
    subgraph "User Interface Layer"
        CLI[Command Line Tools]
        API[REST API]
        LIB[Python Library]
    end

    subgraph "Core Layer"
        ARD[ARD Class<br/>Main Entry Point]
        CONFIG[ARDConfig<br/>Configuration]
    end

    subgraph "Handler Layer"
        ALLELE[AlleleHandler]
        GL[GLStringHandler]
        MAC[MACHandler]
        SERO[SerologyHandler]
        V2[V2Handler]
        XX[XXHandler]
        SN[ShortNullHandler]
    end

    subgraph "Strategy Layer"
        FACTORY[StrategyFactory]
        G[GGroupReducer]
        P[PGroupReducer]
        LG[LGReducer/LGXReducer]
        W[WReducer]
        U2[U2Reducer]
        S[SReducer]
        EXON[ExonReducer]
    end

    subgraph "Data Layer"
        DR[DataRepository]
        DB[(SQLite Database)]
        LOADER[Data Loaders]
    end

    CLI --> ARD
    API --> ARD
    LIB --> ARD
    ARD --> CONFIG
    ARD --> ALLELE
    ARD --> GL
    ARD --> MAC
    ARD --> SERO
    ARD --> V2
    ARD --> XX
    ARD --> SN

    ALLELE --> FACTORY
    FACTORY --> G
    FACTORY --> P
    FACTORY --> LG
    FACTORY --> W
    FACTORY --> U2
    FACTORY --> S
    FACTORY --> EXON

    ARD --> DR
    DR --> DB
    DR --> LOADER
    LOADER --> DB
```

---

## Core Components

### 1. ARD Class (`pyard/ard.py`)

The main entry point and orchestrator for all HLA reduction operations.

**Responsibilities:**
- Initialize database connections and load reference data
- Coordinate between handlers for different typing formats
- Manage caching for performance optimization
- Provide public API for reduction operations

**Key Methods:**
- `redux(glstring, redux_type)` - Main reduction method
- `expand_mac(mac_code)` - Expand MAC codes
- `lookup_mac(allele_list)` - Find MAC for allele list
- `validate(glstring)` - Validate GL strings
- `cwd_redux(allele_list)` - CWD reduction

### 2. Configuration (`pyard/config.py`)

```mermaid
classDiagram
    class ARDConfig {
        +bool reduce_serology
        +bool reduce_v2
        +bool reduce_3field
        +bool reduce_P
        +bool reduce_XX
        +bool reduce_MAC
        +bool reduce_shortnull
        +bool ping
        +bool verbose_log
        +bool ARS_as_lg
        +bool strict
        +tuple ignore_allele_with_suffixes
        +from_dict(config_dict) ARDConfig
        +to_dict() dict
    }
```

Manages all configuration options for reduction behavior.

### 3. Handlers (`pyard/handlers/`)

Specialized handlers for different typing formats:

```mermaid
graph LR
    ARD[ARD Instance] --> AH[AlleleHandler<br/>Core allele reduction]
    ARD --> GH[GLStringHandler<br/>GL String parsing]
    ARD --> MH[MACHandler<br/>MAC code operations]
    ARD --> SH[SerologyHandler<br/>Serology mapping]
    ARD --> VH[V2Handler<br/>V2 to V3 conversion]
    ARD --> XH[XXHandler<br/>XX code expansion]
    ARD --> SNH[ShortNullHandler<br/>Short null handling]
```

**AlleleHandler** - Delegates to reduction strategies via StrategyFactory
**GLStringHandler** - Parses and processes GL Strings with delimiters (`/`, `+`, `^`, `~`)
**MACHandler** - Expands and looks up MAC (Multiple Allele Codes)
**SerologyHandler** - Maps serology to alleles and handles broad/split relationships
**V2Handler** - Converts V2 allele names to V3 format
**XXHandler** - Expands XX codes to allele lists
**ShortNullHandler** - Handles short null alleles (e.g., `A*01:01N`)

---

## Data Flow

### Reduction Flow

```mermaid
sequenceDiagram
    participant User
    participant ARD
    participant GLHandler
    participant AlleleHandler
    participant StrategyFactory
    participant Reducer
    participant Database

    User->>ARD: redux("A*01:01:01:01", "G")
    ARD->>GLHandler: process_gl_string()
    GLHandler-->>ARD: Not a GL string
    ARD->>AlleleHandler: reduce_allele()
    AlleleHandler->>StrategyFactory: get_strategy("G")
    StrategyFactory-->>AlleleHandler: GGroupReducer
    AlleleHandler->>Reducer: reduce("A*01:01:01:01")
    Reducer->>Database: lookup G group mapping
    Database-->>Reducer: "A*01:01:01G"
    Reducer-->>AlleleHandler: "A*01:01:01G"
    AlleleHandler-->>ARD: "A*01:01:01G"
    ARD-->>User: "A*01:01:01G"
```

### Initialization Flow

```mermaid
sequenceDiagram
    participant User
    participant Init
    participant ARD
    participant DB
    participant DataRepo
    participant Loaders

    User->>Init: pyard.init("3510")
    Init->>ARD: __init__()
    ARD->>DB: create_db_connection()
    DB-->>ARD: connection

    alt Database exists
        ARD->>DB: load_ars_mappings()
        ARD->>DB: load_code_mappings()
        ARD->>DB: load_serology_mappings()
    else Database doesn't exist
        ARD->>DataRepo: generate_ard_mapping()
        DataRepo->>Loaders: load_g_group()
        DataRepo->>Loaders: load_p_group()
        Loaders-->>DataRepo: data
        DataRepo->>DB: save_ars_mappings()
        DataRepo->>DB: save_code_mappings()
    end

    ARD->>ARD: initialize_handlers()
    ARD->>ARD: setup_caching()
    ARD-->>Init: ard instance
    Init-->>User: ard instance
```

---

## Module Details

### Data Repository (`pyard/data_repository.py`)

Manages data loading and transformation from IPD-IMGT/HLA releases.

**Key Functions:**
- `generate_ard_mapping()` - Creates G/P/lgx/exon group mappings
- `generate_alleles_and_xx_codes_and_who()` - Generates allele lists and XX codes
- `generate_serology_mapping()` - Creates serology to allele mappings
- `generate_mac_codes()` - Loads MAC codes from NMDP service
- `generate_short_nulls()` - Creates short null mappings
- `generate_cwd_mapping()` - Loads CWD allele lists

### Database Layer (`pyard/db.py`)

SQLite database operations for persistent storage.

**Key Tables:**
- `g_group` - G group mappings
- `p_group` - P group mappings
- `lgx_group` - lgx group mappings
- `exon_group` - Exon mappings
- `alleles` - Valid alleles
- `who_alleles` - WHO nomenclature alleles
- `mac_codes` - MAC code expansions
- `serology_mapping` - Serology to allele mappings
- `xx_codes` - XX code expansions
- `shortnulls` - Short null mappings
- `cwd2` - CWD Version 2 alleles
- `v2_mapping` - V2 to V3 conversions

### Reducers (`pyard/reducers/`)

Strategy pattern implementation for different reduction types.

```mermaid
classDiagram
    class Reducer {
        <<abstract>>
        +ARD ard
        +reduce(allele: str) str*
    }

    class GGroupReducer {
        +reduce(allele: str) str
    }

    class PGroupReducer {
        +reduce(allele: str) str
    }

    class LGReducer {
        +reduce(allele: str) str
    }

    class LGXReducer {
        +reduce(allele: str) str
    }

    class WReducer {
        +reduce(allele: str) str
    }

    class U2Reducer {
        +reduce(allele: str) str
    }

    class SReducer {
        +reduce(allele: str) str
    }

    class ExonReducer {
        +reduce(allele: str) str
    }

    Reducer <|-- GGroupReducer
    Reducer <|-- PGroupReducer
    Reducer <|-- LGReducer
    Reducer <|-- LGXReducer
    Reducer <|-- WReducer
    Reducer <|-- U2Reducer
    Reducer <|-- SReducer
    Reducer <|-- ExonReducer
```

**Reducer Types:**
- **GGroupReducer** - Reduces to G group level (e.g., `A*01:01:01G`)
- **PGroupReducer** - Reduces to P group level (e.g., `A*01:01P`)
- **LGReducer** - Reduces to 2-field with 'g' suffix (e.g., `A*01:01g`)
- **LGXReducer** - Reduces to 2-field without suffix (e.g., `A*01:01`)
- **WReducer** - WHO nomenclature expansion
- **U2Reducer** - 2-field unambiguous reduction
- **SReducer** - Serology reduction (e.g., `A1`)
- **ExonReducer** - 3-field exon reduction

### Loaders (`pyard/loader/`)

Load reference data from IPD-IMGT/HLA releases.

**Modules:**
- `allele_list.py` - Loads allele list from IPD-IMGT/HLA
- `g_group.py` - Loads G group definitions
- `p_group.py` - Loads P group definitions
- `mac_codes.py` - Fetches MAC codes from NMDP service
- `serology.py` - Loads serology mappings
- `cwd.py` - Loads CWD allele lists
- `version.py` - Fetches available IPD-IMGT/HLA versions

---

## Design Patterns

### 1. Strategy Pattern

Used for reduction algorithms to allow runtime selection of reduction strategy.

```mermaid
graph TB
    Client[AlleleHandler] --> Factory[StrategyFactory]
    Factory --> Strategy1[GGroupReducer]
    Factory --> Strategy2[PGroupReducer]
    Factory --> Strategy3[LGReducer]
    Factory --> Strategy4[Other Reducers...]

    Strategy1 -.implements.-> Interface[Reducer Interface]
    Strategy2 -.implements.-> Interface
    Strategy3 -.implements.-> Interface
    Strategy4 -.implements.-> Interface
```

**Benefits:**
- Easy to add new reduction types
- Separation of concerns
- Runtime strategy selection

### 2. Handler Pattern

Specialized handlers for different typing formats.

**Benefits:**
- Single responsibility principle
- Easier testing and maintenance
- Clear separation of concerns

### 3. Repository Pattern

DataRepository abstracts data access and transformation.

**Benefits:**
- Decouples business logic from data access
- Centralized data management
- Easier to test with mock data

### 4. Factory Pattern

StrategyFactory creates appropriate reducer instances.

**Benefits:**
- Centralized object creation
- Encapsulates instantiation logic
- Easy to extend with new strategies

---

## Database Schema

```mermaid
erDiagram
    ALLELES {
        string allele PK
    }

    G_GROUP {
        string allele PK
        string g
    }

    P_GROUP {
        string allele PK
        string p
    }

    LGX_GROUP {
        string allele PK
        string lgx
    }

    MAC_CODES {
        string code PK
        string alleles
    }

    SEROLOGY_MAPPING {
        string serology PK
        string allele_list
        string lgx_allele_list
        string xx
    }

    XX_CODES {
        string allele_1d PK
        string allele_list
    }

    WHO_GROUP {
        string who PK
        string allele_list
    }

    V2_MAPPING {
        string v2 PK
        string v3
    }

    CWD2 {
        string allele PK
        string locus
    }

    ALLELES ||--o{ G_GROUP : "maps to"
    ALLELES ||--o{ P_GROUP : "maps to"
    ALLELES ||--o{ LGX_GROUP : "maps to"
```

---

## Extension Points

### Adding a New Reduction Type

1. **Create a new reducer class** in `pyard/reducers/`:

```python
from .base_reducer import Reducer

class MyCustomReducer(Reducer):
    def reduce(self, allele: str) -> str:
        # Implement custom reduction logic
        return reduced_allele
```

2. **Register in StrategyFactory** (`pyard/reducers/reducer_factory.py`):

```python
def _initialize_strategies(self):
    self._strategies = {
        # ... existing strategies
        "CUSTOM": MyCustomReducer(self.ard),
    }
```

3. **Update constants** (`pyard/constants.py`):

```python
VALID_REDUCTION_TYPE = Literal["G", "P", "lg", "lgx", "W", "exon", "U2", "S", "CUSTOM"]
```

### Adding a New Handler

1. **Create handler class** in `pyard/handlers/`:

```python
class MyHandler:
    def __init__(self, ard_instance):
        self.ard = ard_instance

    def process(self, input_data):
        # Implement handler logic
        pass
```

2. **Initialize in ARD class** (`pyard/ard.py`):

```python
def _initialize_handlers(self):
    # ... existing handlers
    self.my_handler = MyHandler(self)
```

### Adding New Data Sources

1. **Create loader** in `pyard/loader/`:

```python
def load_my_data(imgt_version):
    # Fetch and parse data
    return data_table
```

2. **Add to DataRepository** (`pyard/data_repository.py`):

```python
def generate_my_mapping(db_connection, imgt_version):
    if not db.table_exists(db_connection, "my_table"):
        data = load_my_data(imgt_version)
        db.save_dict(db_connection, "my_table", data, ("key", "value"))
```

3. **Call during initialization** in `ARD._initialize_database()`.

---

## Command-Line Tools

### Tool Architecture

```mermaid
graph TB
    subgraph "CLI Tools"
        PYARD[pyard<br/>Quick reduction]
        IMPORT[pyard-import<br/>Database import]
        STATUS[pyard-status<br/>Database status]
        REDUCE[pyard-reduce-csv<br/>Batch processing]
    end

    PYARD --> ARD[ARD Library]
    IMPORT --> DR[DataRepository]
    STATUS --> DB[Database Layer]
    REDUCE --> ARD

    DR --> DB
    ARD --> DB
```

**Tools:**
- `pyard` - Interactive reduction tool
- `pyard-import` - Import/update IPD-IMGT/HLA database
- `pyard-status` - Show database status and statistics
- `pyard-reduce-csv` - Batch process CSV files

---

## REST API Architecture

```mermaid
graph TB
    Client[HTTP Client] --> Flask[Flask/Connexion App]
    Flask --> API[API Module]
    API --> ARD[ARD Instance]
    ARD --> DB[(SQLite Database)]

    Flask --> Swagger[Swagger UI]
```

**Endpoints:**
- `POST /redux` - Reduce GL strings
- `POST /expand_mac` - Expand MAC codes
- `POST /lookup_mac` - Lookup MAC for allele list
- `GET /version` - Get database version
- `GET /ui` - Swagger UI

**Deployment:**
- Development: Flask built-in server
- Production: Gunicorn/Uvicorn with Docker

---

## Performance Considerations

### Caching Strategy

```mermaid
graph LR
    A[User Request] --> B{In Cache?}
    B -->|Yes| C[Return Cached Result]
    B -->|No| D[Compute Result]
    D --> E[Store in Cache]
    E --> F[Return Result]
```

**Cached Methods:**
- `redux()` - Main reduction method
- `_redux_allele()` - Core allele reduction
- `is_mac()` - MAC validation
- `smart_sort_comparator()` - Sorting comparator

**Cache Size:**
- Default: 1,000 entries
- Configurable via `cache_size` parameter
- LRU (Least Recently Used) eviction policy

### Database Optimization

- **Read-only connections** for thread safety
- **Indexed lookups** on primary keys
- **Frozen reference data** (Python 3.9+) for memory efficiency
- **Batch operations** for data loading

---

## Testing Architecture

```mermaid
graph TB
    subgraph "Test Types"
        UNIT[Unit Tests<br/>pytest]
        BDD[BDD Tests<br/>behave]
    end

    subgraph "Test Coverage"
        HANDLERS[Handler Tests]
        REDUCERS[Reducer Tests]
        DB[Database Tests]
        INTEGRATION[Integration Tests]
    end

    UNIT --> HANDLERS
    UNIT --> REDUCERS
    UNIT --> DB
    BDD --> INTEGRATION
```

**Test Structure:**
- `tests/unit/` - Unit tests for individual components
- `tests/features/` - BDD feature files
- `tests/steps/` - BDD step implementations

---

## Contributing Guidelines

### Code Organization

1. **Handlers** - Add new typing format handlers in `pyard/handlers/`
2. **Reducers** - Add new reduction strategies in `pyard/reducers/`
3. **Loaders** - Add new data loaders in `pyard/loader/`
4. **Utilities** - Add helper functions in `pyard/misc.py`

### Best Practices

- Follow existing code style and patterns
- Add type hints for new functions
- Write unit tests for new functionality
- Update documentation for API changes
- Use descriptive variable and function names
- Keep functions focused and single-purpose

### Development Workflow

1. Fork and clone repository
2. Create virtual environment: `make venv`
3. Install dependencies: `make install`
4. Make changes and add tests
5. Run tests: `make test`
6. Submit pull request

---

## Glossary

- **ARD** - Antigen Recognition Domain
- **HLA** - Human Leukocyte Antigen
- **IPD-IMGT/HLA** - International ImMunoGeneTics HLA Database
- **MAC** - Multiple Allele Code
- **GL String** - Genotype List String (format for representing HLA typings)
- **CWD** - Common and Well-Documented alleles
- **G Group** - Group of alleles with identical nucleotide sequences across exons 2 and 3
- **P Group** - Group of alleles with identical protein sequences
- **Serology** - Serological antigen typing (older HLA typing method)
- **V2/V3** - Version 2/Version 3 of HLA nomenclature
- **XX Code** - Placeholder for all alleles at a given resolution

---

## Additional Resources

- [IPD-IMGT/HLA Database](https://www.ebi.ac.uk/ipd/imgt/hla/)
- [HLA Nomenclature](http://hla.alleles.org/nomenclature/index.html)
- [GL String Specification](https://glstring.org/)
- [NMDP Bioinformatics](https://bioinformatics.bethematchclinical.org/)

---

**Document Version:** 1.0
**Last Updated:** 2024
**Maintainer:** NMDP Bioinformatics Team
