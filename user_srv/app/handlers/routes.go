package handlers

import (
	"net/http"

	guard "github.com/andust/user_service/handlers/guards"
	"github.com/andust/user_service/handlers/middlewares"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

func (h *Handler) Routes(e *echo.Echo) {
	e.Use(middleware.CORSWithConfig(middleware.CORSConfig{
		AllowOrigins:     []string{"http://localhost:4200", "http://localhost:3001"},
		AllowMethods:     []string{http.MethodGet, http.MethodHead, http.MethodPut, http.MethodPatch, http.MethodPost, http.MethodDelete},
		AllowCredentials: true,
	}))

	apiGroup := e.Group("/api/v1")

	apiGroup.POST("/login", h.Login)
	apiGroup.POST("/register", h.Register)

	apiGroup.GET("/token/verify", h.VerifyToken)
	apiGroup.GET("/token/refresh", h.RefreshToken)

	authMiddleware := middlewares.AuthMiddleware{
		ErrorLog:       h.Core.ErrorLog,
		UserRepository: h.Core.Repository.UserRepository,
		RedisClient:    h.Core.RedisClient,
	}

	apiGroup.Use(authMiddleware.IsLoggedIn)

	apiGroup.GET("/logout", h.Logout)
	apiGroup.GET("/user", h.UserDetail)
	// for now only admin have access to user list - just for check if admin guard works
	apiGroup.GET("/users", guard.AdminAuthGuard(h.UsersList))
}
