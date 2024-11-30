# Database
Deployed on AWS S3, Lambda, and DynamoDb

- src/ (Placeholder: all the other folders in APIdb)
- ...


## Temporary Data Schema (Examples: db_tmp.json)

`api_key_flg` is a flag to indicate if the API requires an API key.
    - 0: No API key required
    - 1: API key required
    - 2: API key is optional. For instance, Jira supports anonymous access which has less permissions than an authenticated user.

`ai_tool_desc` this field is tentative and only experiment on Claude calling. Tool calling in openAI has different schema.

## Notes
Can use `openapi-generator` to generate OpenAPI yaml file from other formats like swagger yaml file.
