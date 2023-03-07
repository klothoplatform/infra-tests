package tests

import (
	"net/http"

	"github.com/klothoplatform/mega-app/pkg/persist"
)

func TestReadTextSecret() http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		content, code := persist.ReadSecretDotTxt(r.Context(), "string")
		w.WriteHeader(code)
		w.Write(content)
	}
}

func TestReadBinarySecret() http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		content, code := persist.ReadSecretDotTxt(r.Context(), "bytes")
		w.WriteHeader(code)
		w.Write(content)
	}
}

func TestWriteTextFile() http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		content, code := persist.WriteFromFile(r)
		if code == 200 {
			w.Write([]byte("success"))
		} else {
			w.WriteHeader(code)
			w.Write(content)
		}
	}
}

func TestWriteBinaryFileDirect() http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		content, code := persist.WriteFromBody(r)
		if code == 200 {
			w.Write([]byte("success"))
		} else {
			w.WriteHeader(code)
			w.Write(content)
		}
	}
}

func TestWriteBinaryFileMultipart() http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		content, code := persist.WriteFromFile(r)
		if code == 200 {
			w.Write([]byte("success"))
		} else {
			w.WriteHeader(code)
			w.Write(content)
		}
	}
}

func TestReadTextFile() http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		content, code := persist.ReadFile(r)
		if code == 200 {
			w.Write(content)
		} else {
			w.WriteHeader(code)
			w.Write(content)
		}
	}
}

func TestReadBinaryFile() http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		content, code := persist.ReadFile(r)
		if code == 200 {
			w.Write(content)
		} else {
			w.WriteHeader(code)
			w.Write(content)
		}
	}
}

func TestDeleteFile() http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		code := persist.DeleteFile(r)
		w.WriteHeader(code)
	}
}

func TestReadOrmEnvVarKvEntry() http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		code := persist.ReadOrmEnvVarKvEntry(r)
		w.WriteHeader(code)
	}
}

func TestWriteOrmEnvVarKvEntry() http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		persist.WriteOrmEnvVarKvEntry(r, w)
	}
}
