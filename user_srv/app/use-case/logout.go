package usecase

import (
	"context"

	"github.com/andust/user_service/libs"
)

type logout struct {
	RedisClient libs.MemoryDB
}

func NewLogout(redisClient libs.MemoryDB) logout {
	return logout{RedisClient: redisClient}
}

func (l *logout) Base(userId string) error {
	l.RedisClient.Del(context.Background(), userId)
	return nil
}
