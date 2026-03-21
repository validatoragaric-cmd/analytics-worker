package helpers

import (
	"context"
	"encoding/json"
	"log"
	"net/http"
	"strconv"
	"time"

	"github.com/golang-jwt/jwt/v4"
	"github.com/google/uuid"
)

type response struct {
	Status  int    `json:"status"`
	Message string `json:"message"`
	Errors  []error `json:"errors"`
}

func generateJWTToken(data map[string]interface{}) (string, error) {
    key := []byte("secret")
    token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
        "exp": time.Now().Add(time.Hour * 72).Unix(),
        "sub": data["id"],
    })
    return token.SignedString(key)
}

func isAuthorized(req *http.Request) bool {
	tokenString := req.Header.Get("Authorization")
	token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error {
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, err
		}
		return []byte("secret"), nil
	})
	if err != nil {
		return false
	}
	claims, ok := token.Claims.(jwt.MapClaims)
	if !ok || !token.Valid {
		return false
	}
	expiration, _ := claims["exp"].(float64)
	t := time.Unix(int64(expiration), 0)
	if time.Now().After(t) {
		return false
	}
	return true
}

func generateUUID() string {
    return uuid.New().String()
}

func writeResponse(w http.ResponseWriter, status int, data interface{}) {
	jsonData, err := json.Marshal(data)
	if err != nil {
		log.Println(err)
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	w.Write(jsonData)
}

func writeError(w http.ResponseWriter, err error) {
	w.WriteHeader(http.StatusInternalServerError)
	json.NewEncoder(w).Encode(response{
		Status:  http.StatusInternalServerError,
		Message: "internal server error",
		Errors:  []error{err},
	})
}

func writeJSON(w http.ResponseWriter, data interface{}) {
	jsonData, err := json.Marshal(data)
	if err != nil {
		writeError(w, err)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	w.Write(jsonData)
}

func writeErrorWithStatus(w http.ResponseWriter, status int, err error) {
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(response{
		Status:  status,
		Message: err.Error(),
		Errors:  []error{err},
	})
}