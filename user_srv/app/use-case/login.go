package usecase

import (
	"context"
	"errors"
	"fmt"
	"log"

	"github.com/andust/user_service/constants"
	"github.com/andust/user_service/libs"
	model "github.com/andust/user_service/models"
	"github.com/andust/user_service/repository"
	"github.com/andust/user_service/utils"
)

type login struct {
	ErrorLog       *log.Logger
	UserRepository repository.UserRepository
	RedisClient    libs.MemoryDB
	User           *model.User
}

func NewLogin(logger *log.Logger, userRepository repository.UserRepository, redisClient libs.MemoryDB) login {
	return login{ErrorLog: logger, UserRepository: userRepository, RedisClient: redisClient}
}

func (l *login) Base(email, password string) (string, error) {
	user, err := l.UserRepository.FindOne(repository.UserQuery{Email: email})
	if err != nil {
		l.ErrorLog.Println(err)
		return "", errors.New("unexpected error, please try again")
	}

	if user.IsValidPassword(password) {
		accessToken, err := utils.GenerateJWT(*user, constants.ACCESS_TOKEN_EXP)
		if err != nil {
			l.ErrorLog.Println("accessToken", err)
			return "", errors.New("unexpected error, please try again")
		}
		refreshToken, err := utils.GenerateJWT(*user, constants.REFRESH_TOKEN_EXP)
		if err != nil {
			l.ErrorLog.Println("refreshToken", err)
			return "", errors.New("unexpected error, please try again")
		}
		l.RedisClient.Set(context.Background(), user.ID, refreshToken, constants.REFRESH_TOKEN_EXP)
		l.User = user
		return accessToken, nil
	}

	return "", fmt.Errorf("login user error, please try again")
}
