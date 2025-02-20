package libs

import (
	"context"
	"time"

	"github.com/redis/go-redis/v9"
)

type MemoryDBGet interface {
	Get(ctx context.Context, key string) (string, error)
}

type MemoryDBSet interface {
	Set(ctx context.Context, key string, value interface{}, expiration time.Duration) error
}

type MemoryDBDel interface {
	Del(ctx context.Context, keys ...string) error
}

type MemoryDB interface {
	MemoryDBGet
	MemoryDBSet
	MemoryDBDel
}

type RedisClient struct {
	client *redis.Client
}

func NewRedisClient(addr, password string, db int) (*RedisClient, error) {
	client := redis.NewClient(&redis.Options{
		Addr:     addr,
		Password: password,
		DB:       0,
	})

	_, err := client.Ping(context.Background()).Result()
	if err != nil {
		return nil, err
	}

	return &RedisClient{client: client}, nil
}

func (r *RedisClient) Get(ctx context.Context, key string) (string, error) {
	return r.client.Get(ctx, key).Result()
}

func (r *RedisClient) Set(ctx context.Context, key string, value interface{}, expiration time.Duration) error {
	return r.client.Set(ctx, key, value, expiration).Err()
}

func (r *RedisClient) Del(ctx context.Context, keys ...string) error {
	return r.client.Del(ctx, keys...).Err()
}
