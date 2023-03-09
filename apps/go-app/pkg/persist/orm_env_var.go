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
	Key   string `json:"key"`
	Value string `json:"value"`
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
	db.AutoMigrate(&Record{})
	if err != nil {
		panic(err)
	}
	return db
}

func ReadOrmEnvVarKvEntry(req *http.Request, w http.ResponseWriter) {
	key := req.URL.Query().Get("key")
	db := connect()
	record := Record{Key: key}
	result := db.First(&record, "key = ?", key)
	if result.Error != nil {
		fmt.Println(result.Error.Error())
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusOK)
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(record)
}

func WriteOrmEnvVarKvEntry(req *http.Request, w http.ResponseWriter) {
	var rec Record
	err := json.NewDecoder(req.Body).Decode(&rec)
	if err != nil {
		fmt.Println(err.Error())
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
}
