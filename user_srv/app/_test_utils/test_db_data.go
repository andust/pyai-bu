package testutils

import (
	"log"

	"github.com/andust/user_service/core"
	usecase "github.com/andust/user_service/use-case"
)

func SeedUserCollection(c *core.Core) {
	registerUseCase := usecase.NewRegister(c.InfoLog, c.Repository.UserRepository, c.RedisClient)
	_, err := registerUseCase.Base("example@example.com", "test123")
	log.Println("Seed users", err)
}

func DropUserCollection(c *core.Core) {
	err := c.Repository.UserRepository.Drop("yes")
	log.Println("Drop users", err)
}
