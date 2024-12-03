## pyai

This project is a web application built using FastAPI and Next.js and utilizes the OpenAI API for chatting.

## Technologies

- **FastAPI**: A fast framework for building APIs in Python.
- **Next.js**: A framework for building React applications with server-side rendering.
- **MongoDB**: A NoSQL database that stores data in JSON format.
- **Qdrant**: An efficient vector database for storing and searching data.

## Features

- The application supports user interactions through chat.
- Scrape and extract data from websites.
- Upload files.
- Query the contents of files and web pages with ease.
- Generage images by OpenAI API.

## Instructions

1. Create a `.env` file in the `genai_srv` folder and add your OpenAI API key as follows:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

2. Rename `user_srv/app/dev-data.example.json` to `user_srv/app/dev-data.json`.

3. Run the application using Docker Compose:
   ```
   docker-compose up
   ```

4. In the Makefile, execute the script to build the application:
   ```
   make build-script
   ```

5. Run the script to migrate developer data:
   ```
   make user-scripts-migrate-dev-data
   ```

## Plan

- Remove useless data from web scraper results.
- Group web scraper results by domain. 
- Group analyzer.
- Improve the chat interface UI.

## License

This project is licensed under the MIT License.