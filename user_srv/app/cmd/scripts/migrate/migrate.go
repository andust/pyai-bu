package migrate

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"os"

	"github.com/andust/user_service/core"
	model "github.com/andust/user_service/models"
	usecase "github.com/andust/user_service/use-case"
)

func MigrateDevData(c *core.Core, args ...string) {

	registerUseCase := usecase.NewRegister(c.ErrorLog, c.Repository.UserRepository, c.RedisClient)

	jsonFile, err := os.Open("dev-data.json")
	if err != nil {
		c.ErrorLog.Fatalln(err)
	}
	defer jsonFile.Close()

	byteValue, err := io.ReadAll(jsonFile)
	if err != nil {
		c.ErrorLog.Fatalln(err)
	}

	var users []struct {
		Username string         `json:"username"`
		Email    string         `json:"email"`
		Password string         `json:"password"`
		Role     model.UserRole `json:"role"`
	}
	if err := json.Unmarshal(byteValue, &users); err != nil {
		log.Fatalf("Parsing JSON error: %s", err)
	}
	for _, user := range users {
		// TODO add more fields - role, username ect.
		result, err := registerUseCase.Base(user.Email, user.Password)

		if err != nil {
			c.ErrorLog.Fatalln(err)
		}
		fmt.Printf("user with id %s inserted", result.ID)
	}
	c.InfoLog.Println("dev data inserted")
}
