package tests

import (
	"net/http"

	"github.com/go-chi/chi/v5"
)

func TestExposePathParam() http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		param := chi.URLParam(r, "param")
		w.Write([]byte(param))
	}
}
