package guards

import (
	"fmt"
	"net/http"
	"slices"

	model "github.com/andust/user_service/models"
	"github.com/labstack/echo/v4"
)

func AdminAuthGuard(next echo.HandlerFunc) echo.HandlerFunc {
	accessRoles := []string{string(model.SuperAdminRole), string(model.AdminRole)}
	return func(c echo.Context) error {
		role := fmt.Sprint(c.Get("role"))
		if !slices.Contains(accessRoles, role) {
			return echo.NewHTTPError(http.StatusForbidden, nil)
		}
		return next(c)
	}
}
