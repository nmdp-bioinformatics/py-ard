# WMDA Data Files — Architecture & Data Model

[//]: # (Prepared with Q Developer)

## Overview

The IPD-IMGT/HLA WMDA data files provide machine-readable representations of the WHO HLA Nomenclature system. They
document relationships between serologically defined antigens and DNA-based allele sequences. These files are released
quarterly alongside new IPD-IMGT/HLA Database versions.

**Source:** IPD-IMGT/HLA Database v3.64.0
**Format:** Semicolon-delimited (`;`) text files
**Encoding:** ASCII

---

## Common File Header

All files share a 6-line header:

```
# file: <filename>
# date: <YYYY-MM-DD>
# version: IPD-IMGT/HLA <version>
# origin: <URL>
# repository: <URL>
# author: <author>
```

---

## File Descriptions & Data Models

### 1. `hla_nom.txt` — HLA Nomenclature

Master registry of all current and deleted HLA antigens and alleles.

**Fields (6, semicolon-separated):**

| # | Field         | Type     | Description                                  | Example              |
|---|---------------|----------|----------------------------------------------|----------------------|
| 1 | Locus         | String   | HLA locus (A, B, Cw, DR, DQ, A*, B*, etc.)   | `A` or `A*`          |
| 2 | Name          | String   | Antigen number or allele designation         | `1` or `01:01:01:01` |
| 3 | Date Assigned | YYYYMMDD | Date the name was assigned                   | `19680101`           |
| 4 | Date Deleted  | YYYYMMDD | Date deleted (empty if current)              | `20010717`           |
| 5 | Identical To  | String   | Allele shown to be identical to (if deleted) | `01:04:01:01N`       |
| 6 | Reason        | String   | Reason for deletion                          | `Sequence identical` |

**Key observations:**

- Antigens use locus without `*` (e.g., `A;1;...`)
- Alleles use locus with `*` (e.g., `A*;01:01:01:01;...`)
- Sorted by locus, then by antigen/allele number

```
┌─────────────────────────────────────────────────────────────────────┐
│                         hla_nom.txt                                 │
├─────────┬──────────────┬──────────┬──────────┬────────────┬─────────┤
│  Locus  │    Name      │ Assigned │ Deleted  │IdenticalTo │ Reason  │
├─────────┼──────────────┼──────────┼──────────┼────────────┼─────────┤
│ A       │ 1            │19680101  │          │            │         │
│ A       │ 2            │19680101  │          │            │         │
│ A*      │ 01:01:01:01  │19891101  │          │            │         │
│ A*      │ 0105N        │19990216  │20010717  │01:04:01:01N│Seq ident│
└─────────┴──────────────┴──────────┴──────────┴────────────┴─────────┘
```

---

### 2. `hla_nom_g.txt` — G Groups (Nucleotide-level)

Groups alleles with identical nucleotide sequences across peptide-binding domain exons (exons 2+3 for Class I, exon 2
for Class II).

**Fields (3, semicolon-separated):**

| # | Field        | Type   | Description                                           | Example                        |
|---|--------------|--------|-------------------------------------------------------|--------------------------------|
| 1 | Locus        | String | HLA locus with `*`                                    | `A*`                           |
| 2 | Allele List  | String | `/`-separated allele names in the group               | `01:01:01:01/01:01:01:02N/...` |
| 3 | G Group Name | String | Group designation (empty if allele is not in a group) | `01:01:01G`                    |

**Key observations:**

- Lines with a G group name contain all member alleles in field 2
- Lines with an empty G group name are alleles not belonging to any group
- Allele suffixes: `N` = Null, `L` = Low expression, `Q` = Questionable

```
┌──────────────────────────────────────────────────────────────┐
│                       hla_nom_g.txt                          │
├─────────┬────────────────────────────────────┬───────────────┤
│  Locus  │         Allele List                │  G Group Name │
├─────────┼────────────────────────────────────┼───────────────┤
│ A*      │ 01:01:01:01/01:01:01:02N/01:01:38L │ 01:01:01G     │
│ A*      │ 01:01:02                           │ (empty)       │
│ A*      │ 01:01:03                           │ (empty)       │
└─────────┴────────────────────────────────────┴───────────────┘
```

---

### 3. `hla_nom_p.txt` — P Groups (Protein-level)

Groups alleles with identical protein sequences in the antigen-binding domains (exons 2+3 for Class I, exon 2 for Class
II).

**Fields (3, semicolon-separated):**

| # | Field        | Type   | Description                                 | Example                       |
|---|--------------|--------|---------------------------------------------|-------------------------------|
| 1 | Locus        | String | HLA locus with `*`                          | `A*`                          |
| 2 | Allele List  | String | `/`-separated allele names in the group     | `01:01:01:01/01:01:01:03/...` |
| 3 | P Group Name | String | Group designation (empty if not in a group) | `01:01P`                      |

**Key observations:**

- Same structure as G groups but based on protein (not nucleotide) identity
- Null alleles (`N` suffix) are excluded from P groups
- P group names use 2-field allele designation + `P` suffix

```
┌──────────────────────────────────────────────────────────────┐
│                       hla_nom_p.txt                          │
├─────────┬────────────────────────────────────┬───────────────┤
│  Locus  │         Allele List                │  P Group Name │
├─────────┼────────────────────────────────────┼───────────────┤
│ A*      │ 01:01:01:01/01:01:01:03/.../01:513 │ 01:01P        │
│ A*      │ 01:02:01:01/01:02:01:02/01:412     │ 01:02P        │
│ A*      │ 01:06                              │ (empty)       │
└─────────┴────────────────────────────────────┴───────────────┘
```

---

### 4. `rel_ser_ser.txt` — Serology-to-Serology Relationships

Maps hierarchical relationships between broad, split, and associated antigens.

**Fields (4, semicolon-separated):**

| # | Field               | Type   | Description                             | Example          |
|---|---------------------|--------|-----------------------------------------|------------------|
| 1 | Locus               | String | HLA locus                               | `A`              |
| 2 | Antigen             | String | Broad or split antigen name             | `9`              |
| 3 | Split Antigens      | String | `/`-separated split antigens (if broad) | `23/24`          |
| 4 | Associated Antigens | String | `/`-separated associated antigens       | `0201/0203/0210` |

**Key observations:**

- Only antigens with splits or associated antigens are listed
- A broad antigen has splits in field 3 (e.g., `A;9;23/24;`)
- A split antigen has associated antigens in field 4 (e.g., `A;23;;2301/2304/2424`)
- Associated antigens use 4-digit designations (zero-padded)

```
┌────────────────────────────────────────────────────────────────┐
│                      rel_ser_ser.txt                           │
├─────────┬─────────┬──────────────────┬─────────────────────────┤
│  Locus  │ Antigen │ Split Antigens   │ Associated Antigens     │
├─────────┼─────────┼──────────────────┼─────────────────────────┤
│ A       │ 2       │                  │ 0201/0202/0203/0208/... │
│ A       │ 9       │ 23/24            │                         │
│ A       │ 10      │ 25/26/34/66      │                         │
│ A       │ 23      │                  │ 2301/2304/2424          │
│ B       │ 21      │ 49/50            │ 4005                    │
└─────────┴─────────┴──────────────────┴─────────────────────────┘
```

---

### 5. `rel_dna_ser.txt` — DNA-to-Serology Relationships

Maps each HLA allele to its serologically equivalent antigen(s).

**Fields (7, semicolon-separated):**

| # | Field                | Type   | Description                       | Example       |
|---|----------------------|--------|-----------------------------------|---------------|
| 1 | Locus                | String | HLA locus with `*`                | `A*`          |
| 2 | Allele Name          | String | Full allele designation           | `01:01:01:01` |
| 3 | Unambiguous Serology | String | Confirmed antigen                 | `1`           |
| 4 | Possible Serology    | String | `/`-separated possible antigens   | `0/1`         |
| 5 | Assumed Serology     | String | Inferred antigen from allele name | `1`           |
| 6 | Expert Assigned      | String | Expert-assigned exceptions        |               |
| 7 | HATS Assigned        | String | HATS algorithm assignment         | `1`           |

**Special values:**

- `0` = Null allele (no antigen expressed)
- `?` = No corresponding antigen known
- Empty = No data available for that category

**Key observations:**

- Sorted by locus and allele number
- Only one of fields 3–6 is typically populated per allele
- Field 7 (HATS) is a new addition from the 2026 nomenclature update
- Multiple possible serologies separated by `/`

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                           rel_dna_ser.txt                                    │
├───────┬──────────────┬──────────┬──────────┬─────────┬────────┬──────────────┤
│ Locus │ Allele       │Unambig.  │Possible  │Assumed  │Expert  │ HATS         │
├───────┼──────────────┼──────────┼──────────┼─────────┼────────┼──────────────┤
│ A*    │ 01:01:01:01  │ 1        │          │         │        │ 1            │
│ A*    │ 01:01:01:02N │ 0        │          │         │        │              │
│ A*    │ 01:01:38L    │          │ 0/1      │         │        │ 1            │
│ A*    │ 01:177       │          │          │ 1       │        │ 1            │
│ A*    │ 01:200       │          │          │ 1       │        │ 36           │
└───────┴──────────────┴──────────┴──────────┴─────────┴────────┴──────────────┘
```

---

## Entity Relationship Diagram

```
┌─────────────────────┐         ┌─────────────────────────┐
│     HLA Locus       │         │    Serological Antigen  │
│─────────────────────│         │─────────────────────────│
│ Name (A,B,C,DR,DQ)  │◄────────│ Locus                   │
│                     │         │ Antigen Number          │
│                     │         │ Type: Broad/Split/Assoc │
└────────┬────────────┘         └────────┬────────────────┘
         │                               │
         │ has many                      │ hierarchical
         │                               │ relationships
         ▼                               ▼
┌─────────────────────┐         ┌─────────────────────────┐
│     HLA Allele      │         │   rel_ser_ser.txt       │
│─────────────────────│         │─────────────────────────│
│ Locus*              │         │ Broad ──► Split(s)      │
│ Allele Name         │         │ Split ──► Associated(s) │
│ Date Assigned       │         │ Broad ──► Associated(s) │
│ Date Deleted        │         └─────────────────────────┘
│ Identical To        │
│ Deletion Reason     │
└────────┬────────────┘
         │
         │ belongs to
         ▼
┌─────────────────────────────────────────────────────────┐
│              Allele Groupings                           │
├────────────────────────┬────────────────────────────────┤
│    G Group             │         P Group                │
│    (Nucleotide)        │         (Protein)              │
│────────────────────────│────────────────────────────────│
│ Identical exon 2+3 DNA │ Identical exon 2+3 protein     │
│ Class I: exon 2+3      │ Class I: exon 2+3              │
│ Class II: exon 2       │ Class II: exon 2               │
│ Suffix: G              │ Suffix: P                      │
└────────────────────────┴────────────────────────────────┘
         │
         │ mapped via
         ▼
┌─────────────────────────────────────────────────────────┐
│              rel_dna_ser.txt                            │
│─────────────────────────────────────────────────────────│
│ Allele ──► Unambiguous Serology (confirmed)             │
│ Allele ──► Possible Serology (multiple candidates)      │
│ Allele ──► Assumed Serology (inferred from name)        │
│ Allele ──► Expert Assigned (registry exceptions)        │
│ Allele ──► HATS Assigned (algorithm-calculated)         │
└─────────────────────────────────────────────────────────┘
```

---

## Serology Hierarchy Diagram

```
                    ┌───────────────┐
                    │  Broad Antigen│
                    │   (e.g. A9)   │
                    └───────┬───────┘
                            │
              ┌─────────────┼─────────────┐
              ▼                           ▼
     ┌────────────────┐         ┌────────────────┐
     │ Split Antigen  │         │ Split Antigen  │
     │   (e.g. A23)   │         │   (e.g. A24)   │
     └───────┬────────┘         └──────┬─────────┘
             │                         │
     ┌───────┼───────┐          ┌──────┼──────────────┐
     ▼       ▼       ▼          ▼      ▼              ▼
  ┌──────┐┌──────┐┌──────┐  ┌──────┐┌──────┐     ┌──────┐
  │A2301 ││A2304 ││A2424 │  │A2402 ││A2403 │ ... │A2423 │
  └──────┘└──────┘└──────┘  └──────┘└──────┘     └──────┘
  Associated Antigens        Associated Antigens
```

---

## Allele Grouping Diagram

```
                    ┌──────────────────────┐
                    │   HLA Allele         │
                    │  A*01:01:01:01       │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                                 ▼
   ┌─────────────────────┐          ┌─────────────────────┐
   │  G Group: 01:01:01G │          │  P Group: 01:01P    │
   │  (DNA identity in   │          │  (Protein identity  │
   │   binding exons)    │          │   in binding exons) │
   ├─────────────────────┤          ├─────────────────────┤
   │ A*01:01:01:01       │          │ A*01:01:01:01       │
   │ A*01:01:01:02N      │          │ A*01:01:01:03       │
   │ A*01:01:01:03       │          │ A*01:01:02          │
   │ ...                 │          │ A*01:01:03          │
   │ A*01:01:38L         │          │ ...                 │
   │ A*01:01:51          │          │ A*01:01:38L         │
   │ ...                 │          │ A*01:32             │
   └─────────────────────┘          └─────────────────────┘

   Note: G groups include Null (N) alleles;
         P groups exclude Null alleles (no protein expressed)
```

---

## Data Flow: Allele to Serology Resolution

```
┌──────────────┐     ┌──────────────┐     ┌──────────────────────┐
│  DNA Typing  │────►│ rel_dna_ser  │────►│ Serological Antigen  │
│  (Allele)    │     │  .txt        │     │  Assignment          │
└──────────────┘     └──────────────┘     └──────────┬───────────┘
                                                     │
                                                     ▼
                                          ┌──────────────────────┐
                                          │   rel_ser_ser.txt    │
                                          │   (Hierarchy lookup) │
                                          ├──────────────────────┤
                                          │ Associated → Split   │
                                          │ Split → Broad        │
                                          └──────────────────────┘

Resolution priority:
  1. Unambiguous (field 3) — experimentally confirmed
  2. Possible (field 4) — multiple candidates reported
  3. Assumed (field 5) — inferred from allele name
  4. Expert (field 6) — registry-specific exceptions
  5. HATS (field 7) — algorithm-calculated assignment
```

---

## Allele Name Convention

```
  HLA - A * 01 : 01 : 01 : 01 N
  │     │   │    │    │    │   │
  │     │   │    │    │    │   └─ Expression suffix (N=Null, L=Low, Q=Questionable)
  │     │   │    │    │    └───── Field 4: Synonymous variant (intron/UTR)
  │     │   │    │    └────────── Field 3: Synonymous coding change
  │     │   │    └─────────────── Field 2: Non-synonymous (protein change)
  │     │   └──────────────────── Field 1: Allele group (≈ serological type)
  │     └──────────────────────── Separator (DNA-level typing)
  └────────────────────────────── Gene/Locus
```

---

## File Size Reference (as of version 3640)

| File              | Size   | Records (approx) |
|-------------------|--------|------------------|
| `hla_nom.txt`     | 1.1 MB | ~40,000          |
| `hla_nom_g.txt`   | 513 KB | ~18,000          |
| `hla_nom_p.txt`   | 461 KB | ~16,000          |
| `rel_dna_ser.txt` | 1.0 MB | ~40,000          |
| `rel_ser_ser.txt` | 2.0 KB | ~85              |
| `md5checksum.txt` | 328 B  | 5 checksums      |
