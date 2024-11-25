package main

import (
	"fmt"
	"net/http"
	"os"

	"github.com/andust/user_service/core"
	"github.com/andust/user_service/handlers"
	"github.com/andust/user_service/repository"
	"github.com/labstack/echo-contrib/prometheus"
	"github.com/labstack/echo/v4"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

func main() {
	newCore := core.New()
	serve(newCore)
}

func serve(c *core.Core) {
	c.InfoLog.Println("start server")

	c.InitRepository(os.Getenv("DB_NAME"))
	defer repository.CloseDB()

	c.InitRedisClient()

	e := echo.New()
	h := handlers.Handler{Core: c}
	h.Routes(e)

	p := prometheus.NewPrometheus("user_service", nil)

	p.Use(e)

	http.Handle("/metrics", promhttp.Handler())

	c.ErrorLog.Fatal(e.Start(fmt.Sprintf(":%s", os.Getenv("PORT"))))
}
