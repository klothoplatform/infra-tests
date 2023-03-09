package persist

import (
	"bytes"
	"context"
	"fmt"
	"io"
	"log"
	"net/http"
	"path/filepath"

	"gocloud.dev/blob"
	_ "gocloud.dev/blob/fileblob"
)

func initializeBucket() *blob.Bucket {
	path, err := filepath.Abs("./files")
	if err != nil {
		log.Fatal(err.Error())
	}
	// Create a file-based bucket.
	/**
	* @klotho::persist {
	*	id = "cloudFs"
	* }
	 */
	bucket, err := blob.OpenBucket(context.Background(), fmt.Sprintf("file://%s", path))
	if err != nil {
		log.Fatal(err.Error())
	}
	return bucket
}

func WriteFromFile(req *http.Request) ([]byte, int) {
	path := req.URL.Query().Get("path")
	bucket := initializeBucket()
	defer bucket.Close()
	w, err := bucket.NewWriter(req.Context(), path, nil)
	if err != nil {
		fmt.Printf("Error: %s", err.Error())
		return []byte(err.Error()), http.StatusInternalServerError
	}
	content := receiveFile(req)
	_, writeErr := fmt.Fprint(w, content)
	if writeErr != nil {
		fmt.Printf("Error: %s", err.Error())
		return []byte(writeErr.Error()), http.StatusInternalServerError
	}
	closeErr := w.Close()
	if closeErr != nil {
		fmt.Printf("Error: %s", err.Error())
		return []byte(closeErr.Error()), http.StatusInternalServerError
	}
	fmt.Printf("File with path, %s, written from request file", path)
	return []byte("success"), http.StatusOK
}

func WriteFromBody(req *http.Request) ([]byte, int) {
	path := req.URL.Query().Get("path")
	bucket := initializeBucket()
	defer bucket.Close()
	w, err := bucket.NewWriter(req.Context(), path, nil)
	if err != nil {
		fmt.Printf("Error: %s", err.Error())
		return []byte(err.Error()), http.StatusInternalServerError
	}
	body, err := io.ReadAll(req.Body)
	if err != nil {
		fmt.Printf("Error: %s", err.Error())
		return []byte(err.Error()), http.StatusInternalServerError
	}
	_, writeErr := fmt.Fprint(w, string(body))
	if writeErr != nil {
		fmt.Printf("Error: %s", err.Error())
		return []byte(writeErr.Error()), http.StatusInternalServerError
	}
	closeErr := w.Close()
	if closeErr != nil {
		fmt.Printf("Error: %s", err.Error())
		return []byte(closeErr.Error()), http.StatusInternalServerError
	}
	fmt.Printf("File with path, %s, written from request body", path)
	return []byte("success"), http.StatusOK
}

func ReadFile(req *http.Request) ([]byte, int) {
	path := req.URL.Query().Get("path")
	bucket := initializeBucket()
	defer bucket.Close()
	response, err := bucket.NewReader(req.Context(), path, nil)
	if err != nil {
		fmt.Printf("Error: %s", err.Error())
		return []byte(err.Error()), http.StatusInternalServerError
	}
	body, err := io.ReadAll(response)
	if err != nil {
		fmt.Printf("Error: %s", err.Error())
		return []byte(err.Error()), http.StatusInternalServerError
	}
	closeErr := response.Close()
	if closeErr != nil {
		fmt.Printf("Error: %s", err.Error())
		return []byte(closeErr.Error()), http.StatusInternalServerError
	}
	fmt.Printf("File with path, %s, read", path)
	return body, http.StatusOK
}

func DeleteFile(req *http.Request) int {
	path := req.URL.Query().Get("path")
	bucket := initializeBucket()
	defer bucket.Close()
	if err := bucket.Delete(req.Context(), path); err != nil {
		fmt.Printf("Error: %s", err.Error())
		return http.StatusInternalServerError
	}
	fmt.Printf("File with path, %s, deleted", path)
	return http.StatusOK
}

func receiveFile(r *http.Request) string {
	r.ParseMultipartForm(32 << 20) // limit your max input length
	var buf bytes.Buffer
	file, _, err := r.FormFile("file")
	if err != nil {
		panic(err)
	}
	defer file.Close()
	io.Copy(&buf, file)
	return buf.String()
}
