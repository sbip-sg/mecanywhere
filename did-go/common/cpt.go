package common

import (
	"encoding/json"
	"meca_did/constant"
)

func IsCptJsonSchemaValid(cptJsonSchema string) bool {
	if len(cptJsonSchema) == 0 || len(cptJsonSchema) > constant.JSON_SCHEMA_MAX_LENGTH {
		return false
	}
	return json.Unmarshal([]byte(cptJsonSchema), &map[string]interface{}{}) == nil
}
