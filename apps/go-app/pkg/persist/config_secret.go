package persist

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"path/filepath"

	"gocloud.dev/runtimevar"
	_ "gocloud.dev/runtimevar/filevar"
)

func initializeSecret(decoder string) *runtimevar.Variable {
	path, err := filepath.Abs("secrets/secret.txt")
	if err != nil {
		log.Fatal(err.Error())
	}
	/**
	* @klotho::config {
	*	id = "mySecret"
	*   secret = true
	* }
	 */
	v, err := runtimevar.OpenVariable(context.TODO(), fmt.Sprintf("file://%s?decoder=%s", path, decoder))
	if err != nil {
		log.Fatal(err.Error())
	}
	return v
}

func ReadSecretDotTxt(context context.Context, decoder string) ([]byte, int) {
	v := initializeSecret(decoder)
	defer v.Close()
	snapshot, err := v.Latest(context)
	if err != nil {
		return []byte(err.Error()), http.StatusInternalServerError
	}
	secretValueString, ok := snapshot.Value.(string)
	if ok {
		return []byte(secretValueString), http.StatusOK
	}
	secretValueByte, ok := snapshot.Value.([]byte)
	if ok {
		return secretValueByte, http.StatusOK
	}
	return []byte("Incorrect Secret Types"), http.StatusInternalServerError
}
