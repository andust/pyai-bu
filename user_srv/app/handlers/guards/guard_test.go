package guards

import (
	"net/http"
	"net/http/httptest"
	"testing"

	model "github.com/andust/user_service/models"
	"github.com/labstack/echo/v4"
	"github.com/stretchr/testify/assert"
)

// go test -v -timeout 30s -run ^TestAdminAuthGuard$ github.com/andust/user_service/handlers/guards
func TestAdminAuthGuard(t *testing.T) {
	e := echo.New()

	tests := []struct {
		name               string
		role               model.UserRole
		expectedStatusCode int
	}{
		{
			"Super admin role ok", model.SuperAdminRole, http.StatusOK,
		},
		{
			"Admin role ok", model.AdminRole, http.StatusOK,
		},
		{
			"Client role forbidden", model.ClientRole, http.StatusForbidden,
		},
		{
			"Other role", "other-role", http.StatusForbidden,
		},
		{
			"No role", "", http.StatusForbidden,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			req := httptest.NewRequest(http.MethodGet, "/", nil)
			rec := httptest.NewRecorder()
			c := e.NewContext(req, rec)

			c.Set("role", tt.role)

			handler := AdminAuthGuard(func(c echo.Context) error {
				return c.String(http.StatusOK, "success")
			})

			err := handler(c)
			if tt.expectedStatusCode == http.StatusForbidden {
				assert.Error(t, err)
				he, _ := err.(*echo.HTTPError)
				assert.Equal(t, tt.expectedStatusCode, he.Code)
			} else {
				assert.NoError(t, err)
				assert.Equal(t, http.StatusOK, rec.Code)
				assert.Equal(t, "success", rec.Body.String())
			}
		})
	}
}
