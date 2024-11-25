package libs

import (
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promauto"
)

var RefreshTokenCounter = promauto.NewCounter(prometheus.CounterOpts{
	Name: "user_refresh_token_counter",
	Help: "Total number of requests for user refresh token",
})

var VerifyTokenCounter = promauto.NewCounter(prometheus.CounterOpts{
	Name: "user_verify_token_counter",
	Help: "Total number of requests for user verify token",
})

var LoginCounter = promauto.NewCounter(prometheus.CounterOpts{
	Name: "user_login_counter",
	Help: "Total number of requests for user login",
})
