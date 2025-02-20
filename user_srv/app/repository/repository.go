package repository

import (
	"context"
	"time"

	"go.mongodb.org/mongo-driver/mongo"
)

const DB_TIMEOUT = time.Second * 3

const USER_COLLECTION = "user"

// var db *mongo.Client

type Repository struct {
	Client         *mongo.Client
	UserRepository UserRepository
}

func (r *Repository) CloseDB() {
	r.Client.Disconnect(context.TODO())
}

func collection(client *mongo.Client, databaseName string, collectionName string) *mongo.Collection {
	return client.Database(databaseName).Collection(collectionName)
}

func New(client *mongo.Client, databaseName string) *Repository {
	// db = client

	return &Repository{
		Client:         client,
		UserRepository: NewUserRepository(collection(client, databaseName, USER_COLLECTION)),
	}
}

// func CloseDB() error {
// 	return db.Disconnect(context.TODO())
// }
