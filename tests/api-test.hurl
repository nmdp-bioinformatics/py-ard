# hurl https://hurl.dev/
#
# Run Locally
# hurl --test --variable host=http://localhost:8080 tests/api-test.hurl
#
# Production
# hurl --test --variable host=https://py-ard.nmdp.org tests/api-test.hurl

# ============================================================
# GET /version
# ============================================================

GET {{host}}/version
HTTP 200
[Asserts]
jsonpath "$.ipd_version" isInteger
jsonpath "$.pyard_version" isString


# ============================================================
# POST /redux - lgx reduction
# ============================================================

POST {{host}}/redux
Content-Type: application/json
{
  "gl_string": "A*01:01:01",
  "reduction_method": "lgx"
}
HTTP 200
[Asserts]
jsonpath "$.ard" == "A*01:01"
jsonpath "$.ipd_version" isInteger
jsonpath "$.pyard_version" isString

# POST /redux - G reduction
POST {{host}}/redux
Content-Type: application/json
{
  "gl_string": "A*01:01:01",
  "reduction_method": "G"
}
HTTP 200
[Asserts]
jsonpath "$.ard" == "A*01:01:01G"

# POST /redux - invalid GL String
POST {{host}}/redux
Content-Type: application/json
{
  "gl_string": "INVALID*99:99",
  "reduction_method": "lgx"
}
HTTP 400
[Asserts]
jsonpath "$.message" isString


# ============================================================
# GET /ard/{allele}
# ============================================================

GET {{host}}/ard/DPA1*02:07:01
HTTP 200
[Asserts]
jsonpath "$.allele" == "DPA1*02:07:01"
jsonpath "$.ard" isString
jsonpath "$.ipd_version" isInteger
jsonpath "$.pyard_version" isString

# GET /ard/{allele} - invalid allele
GET {{host}}/ard/INVALID*99:99
HTTP 400
[Asserts]
jsonpath "$.message" isString


# ============================================================
# POST /cwd-redux
# ============================================================

POST {{host}}/cwd-redux
Content-Type: application/json
{
  "gl_string": "A*26:CBJTR"
}
HTTP 200
[Asserts]
jsonpath "$.gl_string" == "A*26:CBJTR"
jsonpath "$.cwd" isString
jsonpath "$.cwd_mac" isString

# POST /cwd-redux - invalid input
POST {{host}}/cwd-redux
Content-Type: application/json
{
  "gl_string": "INVALID*99:99"
}
HTTP 200
[Asserts]
jsonpath "$.message" not exists
jsonpath "$.cwd" == ""
jsonpath "$.cwd_mac" == ""



# ============================================================
# GET /mac/{allele_code} - expand MAC
# ============================================================

GET {{host}}/mac/A*01:AB
HTTP 200
[Asserts]
jsonpath "$.mac" == "A*01:AB"
jsonpath "$.gl_string" isString
jsonpath "$.alleles" isCollection
jsonpath "$.alleles[0]" isString

# GET /mac/{allele_code} - invalid MAC
GET {{host}}/mac/A*01:INVALID
HTTP 404
[Asserts]
jsonpath "$.message" isString


# ============================================================
# POST /mac - lookup MAC from allele list
# ============================================================

POST {{host}}/mac
Content-Type: application/json
{
  "gl_string": "A*01:01/A*01:02"
}
HTTP 200
[Asserts]
jsonpath "$.mac" isString
jsonpath "$.gl_string" == "A*01:01/A*01:02"
jsonpath "$.alleles" isCollection


# ============================================================
# GET /xx/{xx_code} - expand XX code
# ============================================================

GET {{host}}/xx/A*43:XX
HTTP 200
[Asserts]
jsonpath "$.xx_code" == "A*43:XX"
jsonpath "$.gl_string" isString
jsonpath "$.alleles" isCollection
jsonpath "$.alleles[0]" isString

# GET /xx/{xx_code} - invalid XX code
GET {{host}}/xx/A*99:XX
HTTP 404
[Asserts]
jsonpath "$.message" isString


# ============================================================
# POST /validate - valid GL String
# ============================================================

POST {{host}}/validate
Content-Type: application/json
{
  "gl_string": "A*01:01+A*02:01"
}
HTTP 200
[Asserts]
jsonpath "$" == "Yes"

# POST /validate - invalid GL String
POST {{host}}/validate
Content-Type: application/json
{
  "gl_string": "HLA-A*01:BLAH"
}
HTTP 404
[Asserts]
jsonpath "$.valid" == false
jsonpath "$.message" isString
jsonpath "$.cause" isString


# ============================================================
# GET /valid - validate via query param
# ============================================================

GET {{host}}/valid?gl_string=A*01:01%2BA*02:01
HTTP 200
[Asserts]
jsonpath "$" == "Yes"

# GET /valid - invalid GL String
GET {{host}}/valid?gl_string=HLA-A*01:BLAH
HTTP 404
[Asserts]
jsonpath "$.valid" == false
jsonpath "$.message" isString
jsonpath "$.cause" isString


# ============================================================
# POST /blend - DRBX blending
# ============================================================

POST {{host}}/blend
Content-Type: application/json
{
  "DRB1_SLUG": "HLA-DRB1*03:01+HLA-DRB1*04:01",
  "DRB3": "DRB3*01:01",
  "DRB4": "DRB4*01:03",
  "DRB5": ""
}
HTTP 200
[Asserts]
jsonpath "$.DRBX_blend" == "DRB3*01:01+DRB4*01:03"

# POST /blend - missing required DRB1_SLUG
POST {{host}}/blend
Content-Type: application/json
{
  "DRB3": "DRB3*01:01"
}
HTTP 400
[Asserts]
jsonpath "$.title" isString
jsonpath "$.title" == "Bad Request"


# ============================================================
# GET /splits/{allele}
# ============================================================

GET {{host}}/splits/A*10
HTTP 200
[Asserts]
jsonpath "$.broad" == "A*10"
jsonpath "$.splits" isCollection
jsonpath "$.splits" includes "A*25"
jsonpath "$.splits" includes "A*26"

# GET /splits/{allele} - no mapping found
GET {{host}}/splits/A*01:01
HTTP 404
[Asserts]
jsonpath "$.message" isString


# ============================================================
# GET /similar/{allele_prefix}
# ============================================================

GET {{host}}/similar/A*01:9
HTTP 200
[Asserts]
jsonpath "$" isCollection
jsonpath "$[0]" isString

# GET /similar/{allele_prefix} - no matches
GET {{host}}/similar/Z*99:9
HTTP 400
[Asserts]
jsonpath "$.message" isString
