package repository

import (
	"context"
	"fmt"
	"time"

	model "github.com/andust/user_service/models"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
)

type UserRepository interface {
	FindOne(q UserQuery) (*model.User, error)
	FindMany(q UsersQuery) (*[]model.User, error)
	InsertOne(model.User) (*model.User, error)
}

type userRepository struct {
	collection *mongo.Collection
}

func NewUserRepository(collection *mongo.Collection) userRepository {
	return userRepository{
		collection: collection,
	}
}

type UserQuery struct {
	ID    string
	Email string
	Options
}

type UsersQuery struct {
	IDs []string
	Options
}

// func formatObjectIdMultiple(hex []string) ([]primitive.ObjectID, error) {
// 	var list []primitive.ObjectID

//		oids := make([]primitive.ObjectID, len(hex))
//		for _, i := range hex {
//			objectId, err := primitive.ObjectIDFromHex(i)
//			if err != nil {
//				return nil, err
//			}
//			oids = append(oids, objectId)
//			list +
//		}
//		return list, nil
//	}
func (b UserQuery) Filter() bson.D {
	// var filter bson.D
	filter := bson.D{}

	if b.ID != "" {
		if id, err := primitive.ObjectIDFromHex(b.ID); err != nil {
			filter = append(filter, bson.E{
				Key:   "_id",
				Value: id,
			})
		}
	}

	if b.Email != "" {
		filter = append(filter, bson.E{
			Key:   "email",
			Value: b.Email,
		})
	}

	return filter
}

func (u UsersQuery) Filters() bson.M {
	// var filter bson.D
	filter := bson.M{}

	if len(u.IDs) > 0 {
		// objectIDs, err := formatObjectIdMultiple(u.IDs)

		var objectIDs []primitive.ObjectID

		// oids := make([]primitive.ObjectID, len(hex))
		for _, i := range u.IDs {
			objectId, err := primitive.ObjectIDFromHex(i)
			if err != nil {
				return nil
			}
			objectIDs = append(objectIDs, objectId)
		}
		// return list, nil

		filter["_id"] = bson.M{"$in": objectIDs}
		fmt.Println(filter)
		// if err == nil {
		// 	// query := bson.M{"_id": bson.M{"$in": objectIDs}}

		// }
		// if id, err := primitive.ObjectIDFromHex(b.ID); err != nil {
		// 	filter = append(filter, bson.E{
		// 		Key:   "_id",
		// 		Value: id,
		// 	})
		// }
	}

	return filter
}

func (u userRepository) FindOne(q UserQuery) (*model.User, error) {
	ctx, cancel := context.WithTimeout(context.Background(), DB_TIMEOUT)
	defer cancel()

	var user model.User

	filter := q.Filter()
	opts := q.OneEntryOptions()
	err := u.collection.FindOne(ctx, filter, opts).Decode(&user)
	if err != nil {
		return nil, err
	}

	return &user, nil
}

func (u userRepository) FindMany(q UsersQuery) (*[]model.User, error) {
	ctx, cancel := context.WithTimeout(context.Background(), DB_TIMEOUT)
	defer cancel()

	filter := q.Filters()
	opts := q.ManyEntryOptions()
	cursor, err := u.collection.Find(ctx, filter, opts)
	if err != nil {
		return nil, err
	}
	fmt.Println(cursor)
	defer cursor.Close(ctx)

	var users []model.User
	if err = cursor.All(ctx, &users); err != nil {
		fmt.Println(err)
		return nil, err
	}

	return &users, nil
}

func (u userRepository) InsertOne(user model.User) (*model.User, error) {
	ctx, cancel := context.WithTimeout(context.Background(), DB_TIMEOUT)
	defer cancel()

	currentTime := time.Now()
	user.CreatedAt = currentTime
	user.UpdatedAt = currentTime
	insertedResult, err := u.collection.InsertOne(ctx, user)
	if err != nil {
		return nil, err
	}

	if oid, ok := insertedResult.InsertedID.(primitive.ObjectID); ok {
		user.ID = oid.Hex()
	}

	return &user, nil
}

type fakeUserRepository struct {
	users []model.User
}

func NewFakeUserRepository() fakeUserRepository {
	return fakeUserRepository{
		users: []model.User{
			{
				ID: "1",
			},
		},
	}
}

func (f fakeUserRepository) FindOne(q UserQuery) (*model.User, error) {
	var user model.User

	return &user, nil
}
