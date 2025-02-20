package core

import (
	"context"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/andust/user_service/libs"
	"github.com/andust/user_service/repository"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"

	_ "github.com/jackc/pgx/v5/stdlib"

	_ "github.com/golang-migrate/migrate/v4/source/file"
	_ "github.com/lib/pq"
)

type Core struct {
	InfoLog     *log.Logger
	ErrorLog    *log.Logger
	Repository  repository.Repository
	RedisClient libs.MemoryDB
}

func New() *Core {
	return &Core{
		InfoLog:  log.New(os.Stdout, "INFO\t", log.Ldate|log.Ltime),
		ErrorLog: log.New(os.Stdout, "ERROR\t", log.Ldate|log.Ltime|log.Lshortfile),
	}
}

func (c *Core) initDB(host string) (*mongo.Client, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	client, err := mongo.Connect(ctx, options.Client().ApplyURI(host))

	if err != nil {
		c.ErrorLog.Fatalf("initDB: %v", err)
		return nil, err
	}

	err = client.Ping(ctx, nil)

	if err != nil {
		c.ErrorLog.Fatalf("initDB: %v", err)
		return nil, err
	}

	return client, nil
}

func (c *Core) InitRepository(host, databaseName string) error {
	client, err := c.initDB(host)

	if err != nil {
		return err
	}

	c.Repository = *repository.New(client, databaseName)

	return nil
}

func (c *Core) InitRedisClient(host, port, password string) {
	client, err := libs.NewRedisClient(
		fmt.Sprintf("%s:%s", host, port),
		password,
		0,
	)

	if err != nil {
		c.ErrorLog.Fatalf("redis connection problem %v", err)
	}

	c.RedisClient = client
}
