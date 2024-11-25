package migrate

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"os"

	"github.com/andust/user_service/core"
	model "github.com/andust/user_service/models"
)

func MigrateDevData(c *core.Core, args ...string) {
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
		newUser := model.User{
			Username: user.Username,
			Email:    user.Email,
			Password: user.Password,
			Role:     user.Role,
		}
		newUser.HashPassword()

		if !newUser.IsValid() {
			log.Fatal("invalid user to insert")
		}
		insertedUser, err := c.Repository.UserRepository.InsertOne(newUser)
		if err != nil {
			c.ErrorLog.Fatalln(err)
		}
		fmt.Printf("user with id %s inserted", insertedUser.ID)
	}
	c.InfoLog.Println("dev data inserted")
}
