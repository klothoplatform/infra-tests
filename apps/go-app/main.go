package main

import (
	"fmt"
	"net/http"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"github.com/klothoplatform/mega-app/pkg/tests"
)

func main() {
	r := chi.NewRouter()
	r.Use(middleware.Logger)

	r.Get("/", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("Hello!"))
	})

	r.Get("/test/persist-secret/read-text-secret", tests.TestReadTextSecret())
	r.Get("/test/persist-secret/read-binary-secret", tests.TestReadBinarySecret())

	r.Get("/test/persist-fs/read-text-file", tests.TestReadTextFile())
	r.Get("/test/persist-fs/read-binary-file", tests.TestReadBinaryFile())
	r.Post("/test/persist-fs/write-text-file", tests.TestWriteTextFile())
	r.Post("/test/persist-fs/write-binary-file", tests.TestWriteTextFile())
	r.Post("/test/persist-fs/write-binary-file-multipart", tests.TestWriteBinaryFileMultipart())
	r.Post("/test/persist-fs/write-binary-file-direct", tests.TestWriteBinaryFileDirect())
	r.Delete("/test/persist-fs/delete-file", tests.TestDeleteFile())

	r.Get("/test/persist-orm/envvar-read-kv-entry", tests.TestReadOrmEnvVarKvEntry())
	r.Post("/test/persist-orm/envvar-write-kv-entry", tests.TestWriteOrmEnvVarKvEntry())

	fmt.Println("Listening on :3000")

	/* @klotho::expose {
	 *   target = "public"
	 *   id = "go-gateway-primary"
	 * }
	 */
	http.ListenAndServe(":3000", r)
}
