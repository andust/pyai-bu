package middlewares

import (
	"log"
	"net/http"
	"net/http/httptest"
	"os"
	"testing"
	"time"

	testutils "github.com/andust/user_service/_test_utils"
	model "github.com/andust/user_service/models"
	"github.com/andust/user_service/utils"
	"github.com/labstack/echo/v4"
	"github.com/stretchr/testify/assert"
)

var testApp *testutils.TestApp

func TestMain(m *testing.M) {
	testApp = testutils.NewTestApp()
	testApp.SeedTestDB()
	log.Println("do before the test!")

	exitVal := m.Run()

	log.Println("do after the test!")
	testApp.Cleanup()

	os.Exit(exitVal)
}

// go test -v -timeout 30s -run ^TestIsLoggedIn$ github.com/andust/user_service/handlers/middlewares
func TestIsLoggedIn(t *testing.T) {
	user := model.User{
		ID:    "1",
		Email: "test-email@example.com",
		Role:  model.SuperAdminRole,
	}
	valid_jwt, err := utils.GenerateJWT(user, time.Minute*15)
	if err != nil {
		t.Error(err)
	}

	tests := []struct {
		name               string
		token              string
		expectedStatusCode int
	}{
		{"Valid token", valid_jwt, http.StatusOK},
		{"Invalid token", "", http.StatusUnauthorized},
	}

	authMiddleware := AuthMiddleware{
		ErrorLog:       log.New(os.Stdout, "", log.LstdFlags),
		UserRepository: testApp.Core.Repository.UserRepository,
		RedisClient:    testApp.Core.RedisClient,
	}

	e := echo.New()
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {

			// Create a request and response recorder
			req := httptest.NewRequest(http.MethodGet, "/", nil)
			req.AddCookie(utils.NewAccessCookie(tt.token))
			rec := httptest.NewRecorder()
			c := e.NewContext(req, rec)

			// Create a test handler
			testHandler := func(c echo.Context) error {
				return c.String(http.StatusOK, "Logged In")
			}

			// Wrap the test handler with the middleware
			handler := authMiddleware.IsLoggedIn(testHandler)

			// Call the handler
			err := handler(c)

			if tt.expectedStatusCode == http.StatusOK {
				assert.Equal(t, tt.expectedStatusCode, rec.Code)
			} else {
				he, _ := err.(*echo.HTTPError)
				assert.Equal(t, tt.expectedStatusCode, he.Code)
			}
		})
	}
}
