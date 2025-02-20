package testutils

import (
	"os"

	"github.com/andust/user_service/core"
)

type TestApp struct {
	Core *core.Core
}

func NewTestApp() *TestApp {
	newCore := core.New()
	newCore.InitRepository(os.Getenv("SUS_DB_HOST"), os.Getenv("TEST_DB_NAME"))
	newCore.InitRedisClient(
		os.Getenv("TEST_REDIS_HOST"),
		os.Getenv("TEST_REDIS_PORT"),
		os.Getenv("TEST_REDIS_PASS"),
	)

	return &TestApp{
		Core: newCore,
	}
}

func (t *TestApp) Cleanup() {
	t.DropTestDB()
	t.Core.Repository.CloseDB()
}

func (t *TestApp) SeedTestDB() {
	SeedUserCollection(t.Core)
}

func (t *TestApp) DropTestDB() {
	DropUserCollection(t.Core)
}
