package usecase

import (
	"errors"
	"log"

	"github.com/andust/user_service/libs"
	model "github.com/andust/user_service/models"
	"github.com/andust/user_service/repository"
	"go.mongodb.org/mongo-driver/mongo"
)

type register struct {
	ErrorLog       *log.Logger
	UserRepository repository.UserRepository
	RedisClient    libs.MemoryDB
}

func NewRegister(logger *log.Logger, userRepository repository.UserRepository, redisClient libs.MemoryDB) register {
	return register{ErrorLog: logger, UserRepository: userRepository, RedisClient: redisClient}
}

func (r *register) Base(email, password string) (*model.User, error) {
	dbUser, err := r.UserRepository.FindOne(repository.UserQuery{Email: email})
	if err != nil {
		if err != mongo.ErrNoDocuments {
			r.ErrorLog.Println(err)
			return nil, errors.New("unexpected error, please try again")
		}
	}
	if dbUser != nil && dbUser.ID != "" {
		return nil, errors.New("user exist")
	}

	user := model.User{
		Email:    email,
		Password: password,
		Role:     model.ClientRole,
	}
	user.HashPassword()

	newUser, err := r.UserRepository.InsertOne(user)
	if err != nil {
		r.ErrorLog.Println(err)
		return nil, errors.New("can't register user, please try again")
	}

	return newUser, nil
}
