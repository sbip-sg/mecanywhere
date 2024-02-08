package constant

type CptType struct {
	code int
	name string
}

func (c CptType) String() string {
	return c.name
}

func (c CptType) Code() int {
	return c.code
}

var (
	ORIGINAL = CptType{code: 0, name: "original"}
	ZKP      = CptType{code: 1, name: "zkp"}
)
