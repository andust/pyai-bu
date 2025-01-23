from app.constants.chat import QuestionType


CHATS = [
        {
            "_id": "678e149ba74ac80c6182cfe1",
            "user_id": "677b1162d538985a7190b6a1",
            "questions": [
                {
                    "content": "example content 1",
                    "mode": QuestionType.CHAT,
                    "answer": "example answer 1",
                }
            ],
        },
        {
            "_id": "678e149ba74ac80c6182cfe2",
            "user_id": "677b1162d538985a7190b6a1",
            "questions": [
                {
                    "content": "example content 2",
                    "mode": QuestionType.CHAT,
                    "answer": "example answer 2",
                },
                {
                    "content": "example content 2.1",
                    "mode": QuestionType.CHAT,
                    "answer": "example answer 2.1",
                },
            ],
        },
        {
            "_id": "678e149ba74ac80c6182cfe3",
            "user_id": "677b1162d538985a7190b6a1",
            "questions": [
                {
                    "content": "example content 3",
                    "mode": QuestionType.RAG,
                    "answer": "example answer 3",
                },
                {
                    "content": "example content 3.1",
                    "mode": QuestionType.CHAT,
                    "answer": "example answer 3.1",
                },
            ],
        },
        {
            "_id": "678e149ba74ac80c6182cfe4",
            "user_id": "677b1162d538985a7190b6a1",
            "questions": None,
        },
    ]