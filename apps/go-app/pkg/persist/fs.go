package persist

import (
	"bytes"
	"context"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"net/http"
	"path/filepath"

	"github.com/go-chi/chi/v5"
	"gocloud.dev/blob"
	_ "gocloud.dev/blob/fileblob"
)

func initializeBucket() *blob.Bucket {
	path, err := filepath.Abs(".")
	if err != nil {
		log.Fatal("failed to get bucket")
	}
	// Create a file-based bucket.
	/**
	* @klotho::persist {
	*	id = "cloudFs"
	* }
	 */
	bucket, err := blob.OpenBucket(context.Background(), fmt.Sprintf("file://%s", path))
	if err != nil {
		log.Fatal("failed to get bucket")
	}
	return bucket
}

func WriteFromFile(req *http.Request) ([]byte, int) {
	path := chi.URLParam(req, "path")
	bucket := initializeBucket()
	defer bucket.Close()
	w, err := bucket.NewWriter(req.Context(), path, nil)
	if err != nil {
		return []byte(err.Error()), http.StatusInternalServerError
	}
	content := receiveFile(req)
	_, writeErr := fmt.Fprintln(w, content)
	closeErr := w.Close()
	if writeErr != nil {
		return []byte(err.Error()), http.StatusInternalServerError
	}
	if closeErr != nil {
		return []byte(err.Error()), http.StatusInternalServerError

	}
	return []byte("success"), http.StatusOK
}

func WriteFromBody(req *http.Request) ([]byte, int) {
	path := chi.URLParam(req, "path")
	bucket := initializeBucket()
	defer bucket.Close()
	w, err := bucket.NewWriter(req.Context(), path, nil)
	if err != nil {
		return []byte(err.Error()), http.StatusInternalServerError
	}
	_, writeErr := fmt.Fprintln(w, req.Body)
	closeErr := w.Close()
	if writeErr != nil {
		return []byte(err.Error()), http.StatusInternalServerError
	}
	if closeErr != nil {
		return []byte(err.Error()), http.StatusInternalServerError

	}
	return []byte("success"), http.StatusOK
}

func ReadFile(req *http.Request) ([]byte, int) {
	path := chi.URLParam(req, "path")
	bucket := initializeBucket()
	defer bucket.Close()
	response, err := bucket.NewReader(req.Context(), path, nil)
	if err != nil {

		return []byte(err.Error()), http.StatusInternalServerError
	}
	closeErr := response.Close()
	if closeErr != nil {
		return []byte(closeErr.Error()), http.StatusInternalServerError
	}
	body, err := ioutil.ReadAll(response)
	if err != nil {
		return []byte(err.Error()), http.StatusInternalServerError
	}
	return body, http.StatusOK
}

func DeleteFile(req *http.Request) int {
	path := chi.URLParam(req, "path")
	bucket := initializeBucket()
	defer bucket.Close()
	if err := bucket.Delete(req.Context(), path); err != nil {
		return http.StatusInternalServerError
	}
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
