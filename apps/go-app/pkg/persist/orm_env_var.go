package persist

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

type Record struct {
	Key   string
	Value string
}

/**
* @klotho::persist {
*   id = "ormEnvVarDB"
*
*   [environment_variables]
*   ORM_CONNECTION_STRING = "orm.connection_string"
* }
 */

func connect() *gorm.DB {
	db, err := gorm.Open(postgres.Open(os.Getenv("ORM_CONNECTION_STRING")), &gorm.Config{})
	if err != nil {
		panic(err)
	}
	return db
}

func ReadOrmEnvVarKvEntry(req *http.Request) int {
	key := req.URL.Query().Get("key")
	db := connect()
	record := Record{Key: key}
	result := db.First(&record)
	if result.Error != nil {
		fmt.Println(result.Error.Error())
		return http.StatusInternalServerError
	}
	return http.StatusOK
}

func WriteOrmEnvVarKvEntry(req *http.Request, w http.ResponseWriter) {
	var rec Record
	err := json.NewDecoder(req.Body).Decode(&rec)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
	db := connect()
	result := db.Create(&rec)
	if result.Error != nil {
		fmt.Println(result.Error.Error())
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(rec)
}
